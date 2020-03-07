import asyncio
import collections
import ctypes
import dataclasses
import enum
import functools
from multiprocessing.shared_memory import SharedMemory
from numbers import Real
import os
from typing import Iterable, Set

import aioserial
import backoff
from pyudev import Context, Device, Monitor, MonitorObserver
from schema import Optional
from serial.serialutil import SerialException
from serial.tools import list_ports

from runtime.messaging import packet as packetlib
from runtime.messaging.device import (
    DeviceBuffer,
    SmartSensorStructure,
    DeviceEvent,
    SmartSensorCommand,
    get_device_type,
)
from runtime.messaging.connection import Connection, RPCConnection
from runtime.monitoring import log
from runtime.service.base import Service
from runtime.util import POSITIVE_INTEGER, POSITIVE_REAL
from runtime.util.exception import RuntimeBaseException


LOG_CAPTURE = log.LogCapture()
LOGGER = log.get_logger(LOG_CAPTURE)


def is_smart_sensor(device: Device) -> bool:
    """
    Determine whether the USB descriptor belongs to an Arduino Micro (CDC ACM).

    .. _Linux USB Project ID List
        http://www.linux-usb.org/usb.ids
    """
    try:
        vendor_id, product_id, _ = device.properties['PRODUCT'].split('/')
        return int(vendor_id, 16) == 0x2341 and int(product_id, 16) == 0x8037
    except (KeyError, ValueError):
        return False


def get_com_ports(devices: Iterable[Device]) -> Iterable[str]:
    """ Translate a sequence of udev devices into COM ports. """
    ports = list_ports.comports(include_links=True)
    for device in devices:
        for filename in os.listdir(device.sys_path):
            if filename.startswith('tty'):
                for port in ports:
                    if port.location in device.sys_path:
                        yield port.device
                        break


class HotplugAction(enum.Enum):
    ADD = enum.auto()
    REMOVE = enum.auto()
    BIND = enum.auto()
    UNBIND = enum.auto()


HotplugEvent = collections.namedtuple('HotplugEvent', ['action', 'device_path', 'ports'])


class SmartSensorObserver(MonitorObserver):
    """
    A background thread for monitoring low-level USB events asynchronously
    using `udev`.

    Event data related to smart sensors are put into a queue for consumption by
    the main thread.
    """

    def __init__(self, hotplug_queue: asyncio.Queue, name: str = 'smart-sensor-observer',
                 subsystem: str = 'usb', device_type: str = 'usb_interface'):
        self.hotplug_queue = hotplug_queue
        self.subsystem, self.device_type = subsystem, device_type
        # We need to store the event loop of the main thread.
        self.loop = asyncio.get_running_loop()
        self.context = Context()
        monitor = Monitor.from_netlink(self.context)
        monitor.filter_by(subsystem, device_type)
        super().__init__(monitor, self.handle_hotplug_event, name=name)

    def handle_initial_sensors(self):
        """ Simulate `udev` ADD/BIND events for all sensors that are already plugged in. """
        for device in self.context.list_devices(subsystem=self.subsystem):
            self.handle_hotplug_event(HotplugAction.ADD.name.lower(), device)
            self.handle_hotplug_event(HotplugAction.BIND.name.lower(), device)

    def handle_hotplug_event(self, action, device):
        event = HotplugEvent(HotplugAction[action.upper()], device.device_path, [])
        if is_smart_sensor(device):
            if event.action is HotplugAction.ADD:
                event.ports.extend(get_com_ports({device}))
            self.loop.call_soon_threadsafe(self.hotplug_queue.put_nowait, event)


@dataclasses.dataclass
class SmartSensor:
    """
    A Smart Sensor and an implementation of its initialize/read/write protocols.
    """
    serial_conn: aioserial.AioSerial
    event_queue: asyncio.Queue
    command_queue: asyncio.Queue = dataclasses.field(default_factory=asyncio.Queue)
    write_interval: Real = 0.05
    terminate_timeout: Real = 2
    ready: asyncio.Event = dataclasses.field(default_factory=asyncio.Event, init=False)
    rtt_down: asyncio.Event = dataclasses.field(default_factory=asyncio.Event, init=False)
    buffer: DeviceBuffer = dataclasses.field(default=None, init=False)

    RTT_ID: int = 0xff

    def __hash__(self):
        return hash(self.serial_conn.port)

    async def initialize_sensor(self, uid: packetlib.SmartSensorUID):
        device_type = get_device_type(uid.device_type)
        device_uid = f'smart-sensor-{uid.to_int()}'
        self.buffer = DeviceBuffer.open(device_type, device_uid, create=True)
        LOGGER.info('Initialized new sensor', device_type=device_type.__name__,
                    device_uid=device_uid)

    async def handle_sub_res(self, packet):
        uid = packet.uid
        if not self.buffer:
            await self.initialize_sensor(uid)
        self.ready.set()

        buf = self.buffer.struct
        buf.subscription, buf.delay = packet.parameter_map, packet.delay
        buf.uid.year, buf.uid.device_type, buf.uid.id = uid.year, uid.device_type, uid.id
        LOGGER.debug('Received subscription request', year=uid.year,
                     device_type=uid.device_type, delay=buf.delay,
                     subscription=[param.name for param in buf.get_parameters(buf.subscription)])

    async def handle_dev_data(self, packet):
        offset, param_buf = 0, memoryview(bytearray(packet.payload[2:]))
        await self.ready.wait()
        for param in self.buffer.struct.get_parameters(packet.parameter_map):
            size = ctypes.sizeof(param.type)
            value = param.type.from_buffer(param_buf[offset: offset + size])
            self.buffer.struct.set_current(param.name, value)
            offset += size
        if offset != len(param_buf):
            raise RuntimeBaseException('DEV_DATA payload contains extra data')

    async def handle_inbound_packet(self, packet):
        if packet.message_id == packetlib.MessageType.HEARTBEAT_REQ:
            response = packetlib.make_heartbeat_res(packet.heartbeat_id)
            await packetlib.send(self.serial_conn, response)
            # LOGGER.debug('Received heartbeat request and sent response',
            #              heartbeat_id=response.heartbeat_id)
        elif packet.message_id == packetlib.MessageType.HEARTBEAT_RES:
            if packet.heartbeat_id == SmartSensor.RTT_ID:
                self.rtt_down.set()
        elif packet.message_id == packetlib.MessageType.DEV_DATA:
            await self.handle_dev_data(packet)
        elif packet.message_id == packetlib.MessageType.SUB_RES:
            await self.handle_sub_res(packet)
        elif packet.message_id == packetlib.MessageType.ERROR:
            pass
        else:
            raise RuntimeBaseException('Packet with bad message ID',
                                       message_id=packet.message_id)

    async def read_loop(self):
        while True:
            try:
                packet = await packetlib.recv(self.serial_conn)
            except packetlib.PacketEncodingException as exc:
                LOGGER.warn('Encountered a packet encoding exception')
            else:
                await self.handle_inbound_packet(packet)

    async def write_loop(self, cycle_period: int = 1000):
        await self.ready.wait()
        loop = asyncio.get_running_loop()
        start, count = loop.time(), 0
        while True:
            await asyncio.sleep(self.write_interval)
            if not self.buffer.struct:
                break

            packet = self.buffer.struct.make_write()
            if packet:
                await packetlib.send(self.serial_conn, packet)
            packet = self.buffer.struct.make_read()
            if packet:
                await packetlib.send(self.serial_conn, packet)

            count = (count + 1) % cycle_period
            if count == 0:
                end = loop.time()
                start, frequency = end, round(cycle_period / (end - start), 3)
                LOGGER.debug('Estimated parameter write frequency',
                             frequency=frequency, uid=self.buffer.struct.uid.to_int())

    @backoff.on_exception(backoff.constant, asyncio.TimeoutError, max_tries=10, logger=LOGGER)
    async def ping(self, timeout: Real = 1):
        """
        Initialize this sensor's data structures and notify all proxies.

         1. The device service pings the sensor to induce a subscription
            response, which contains type and year information.
         2. The device service identifies the structure from the `DEVICES`
            registry.
         3. The device service uses the structure to allocate a shared memory
            block of sufficient size. The device service will be responsible
            for cleaning up this block on disconnect or Runtime exit.
         4. The device service notifies all other services that a new sensor
            has been detected, prompting them to attach to the shared memory
            block. For example, this allows the sensor to be available to
            student code.

        Raises::
            asyncio.TimeoutError: Device never responded with a subscription request.
        """
        await packetlib.send(self.serial_conn, packetlib.make_ping())
        LOGGER.debug('Pinged device', timeout=timeout)
        # Block until the subscription request arrives.
        await asyncio.wait_for(self.ready.wait(), timeout)

    @backoff.on_exception(backoff.constant, Exception, max_tries=10, logger=LOGGER)
    async def disable(self):
        await packetlib.send(self.serial_conn, packetlib.make_disable())
        LOGGER.debug('Disabled device')
        if self.buffer.struct:
            self.buffer.struct.reset()

    async def rtt(self, timeout: Real = 5) -> Real:
        """
        Measure the round-trip time of a packet sent to the Smart Sensor and back.
        """
        loop = asyncio.get_running_loop()
        start = loop.time()
        self.rtt_down.clear()
        await packetlib.send(self.serial_conn, packetlib.make_heartbeat_req(SmartSensor.RTT_ID))
        try:
            await asyncio.wait_for(self.rtt_down.wait(), timeout)
        except asyncio.TimeoutError:
            LOGGER.warn('Never received round-trip-time indicator')
        finally:
            return loop.time() - start

    async def spin(self):
        """ Run this sensor indefinitely. """
        tasks = asyncio.gather(self.ping(), self.read_loop(), self.write_loop())
        try:
            await tasks
        except SerialException as exc:
            LOGGER.error('Serial exception, closing Smart Sensor', exc_info=exc)
        finally:
            tasks.cancel()
            if self.buffer:
                await self.buffer.close(self.terminate_timeout)


@dataclasses.dataclass
class DeviceService(Service):
    sensors: Set = dataclasses.field(default_factory=set)
    event_queue: asyncio.Queue = dataclasses.field(default_factory=asyncio.Queue)

    config_schema = {
        **Service.config_schema,
        Optional('baud_rate', default=115200): POSITIVE_INTEGER,
        Optional('max_hotplug_events', default=128): POSITIVE_INTEGER,
        Optional('broadcast_interval', default=0.2): POSITIVE_REAL,
        Optional('write_interval', default=0.02): POSITIVE_REAL,
        Optional('terminate_timeout', default=2): POSITIVE_REAL,
    }

    def initialize_hotplugging(self):
        """
        Connect all existing sensors and start a thread to detect future hotplug events.

        Returns::
            asyncio.Queue: A queue to hold hotplug events.
        """
        event_queue = asyncio.Queue(self.config['max_hotplug_events'])
        observer = SmartSensorObserver(event_queue)
        observer.handle_initial_sensors()
        observer.start()
        return event_queue

    async def open_serial_connections(self, hotplug_event, **serial_options):
        """ Open a serial connection to a new sensor and schedule its read/write loops. """
        for port in hotplug_event.ports:
            serial_conn = aioserial.AioSerial(port, **serial_options)
            serial_conn.rts = False
            sensor = SmartSensor(
                serial_conn,
                self.event_queue,
                write_interval=self.config['write_interval'],
                terminate_timeout=self.config['terminate_timeout'],
            )
            self.sensors.add(sensor)
            sensor_task = asyncio.create_task(sensor.spin())
            sensor_task.add_done_callback(lambda *_: self.sensors.remove(sensor))

    async def broadcast_status(self):
        """ Periodically notify all other services about currently available sensors. """
        with RPCConnection.open(self.config['sockets']['sensor_status'], logger=LOGGER) as connection:
            while True:
                try:
                    sensors = [sensor.buffer.status for sensor in self.sensors
                               if sensor.ready.is_set() and not sensor.buffer.closing]
                    await connection.notify(DeviceEvent.UPDATE.name, sensors)
                except Exception as exc:
                    LOGGER.error(str(exc), exc_info=exc)
                await asyncio.sleep(self.config['broadcast_interval'])

    async def handle_sensor_command(self, method, *params):
        command = SmartSensorCommand.__members__[method.upper()]
        if command is SmartSensorCommand.PING_ALL:
            await asyncio.gather(*[sensor.ping() for sensor in self.sensors])
        elif command is SmartSensorCommand.DISABLE_ALL:
            await asyncio.gather(*[sensor.disable() for sensor in self.sensors])
        elif command is SmartSensorCommand.REQ_SUB:
            pass
        elif command is SmartSensorCommand.REQ_HEART:
            pass
        elif command is SmartSensorCommand.RTT:
            pass

    async def main(self):
        LOG_CAPTURE.connect(self.log_records)
        with RPCConnection.open(self.config['sockets']['sensor_command'], logger=LOGGER) as cmd_conn:
            asyncio.create_task(self.broadcast_status())
            asyncio.create_task(cmd_conn.dispatch_loop(self.handle_sensor_command))
            event_queue = self.initialize_hotplugging()
            while True:
                hotplug_event = await event_queue.get()
                if hotplug_event.action is HotplugAction.ADD:
                    await self.open_serial_connections(hotplug_event, baudrate=self.config['baud_rate'])