import os from 'os';
import _ from 'lodash';
import RuntimeClient from 'runtime-client';
import { ipcMain } from 'electron';

import RendererBridge from '../RendererBridge';
import { updateConsole } from '../../renderer/actions/ConsoleActions';
import {
  ansibleDisconnect,
  infoPerMessage,
  updateCodeStatus,
} from '../../renderer/actions/InfoActions';
import { updatePeripherals } from '../../renderer/actions/PeripheralActions';
import { robotState, Logger, runtimeState } from '../../renderer/utils/utils';

const getIPAddress = (family = 'IPv4') => {
  const interfaces = os.networkInterfaces();
  let addresses = _.flatten(_.values(interfaces));
  addresses = _.filter(addresses, (address) => address.family === family && !address.internal);
  return _.head(_.map(addresses, ({ address }) => address));
};

const Ansible = {
  logger: new Logger('ansible', 'Ansible Debug'),
  conn: null,
  currentCodeStatus: null,
  async recvDatagrams() {
    try {
      for await (const datagram of this.conn.recvDatagrams()) {
        const sensorData = _.map(datagram.devices, ({ type }, uid) => ({
          device_type: type, uid,
        }));

        if (this.currentCodeStatus === null) {
          RendererBridge.reduxDispatch(infoPerMessage(runtimeState.STUDENT_STOPPED));
          RendererBridge.reduxDispatch(updateCodeStatus(robotState.IDLE));
        } else {
          let status;
          switch (this.currentCodeStatus) {
            case robotState.TELEOP: status = runtimeState.TELEOP; break;
            case robotState.AUTONOMOUS: status = runtimeState.AUTONOMOUS; break;
            case robotState.ESTOP: status = runtimeState.ESTOP; break;
            default: status = runtimeState.STUDENT_STOPPED;
          }
          RendererBridge.reduxDispatch(infoPerMessage(status));
          RendererBridge.reduxDispatch(updatePeripherals(sensorData));
        }
      }
    } catch (e) {
      console.log(e);
    }
  },
  async recvLogs() {
    try {
      for await (const log of this.conn.recvLogs()) {
        if (log.logger === 'runtime.game.studentapi' && log.event) {
          RendererBridge.reduxDispatch(updateConsole(`[${log.timestamp}] ${log.event}\n`));
        }
      }
    } catch (e) {
      console.log(e);
    }
  },
  setup() {
    const host = '127.0.0.1' || getIPAddress(); // TODO

    ipcMain.on('ipAddress', (event, { ipAddress }) => {
      this.close();
      this.conn = new RuntimeClient(ipAddress);
      console.log(`Opened client to ${ipAddress}, receiving on ${host}`);
      return this.conn.connectAll()
        .then(() => Promise.all([
          this.recvDatagrams(this.conn),
          this.recvLogs(this.conn),
        ]));
    });

    // eslint-disable-next-line consistent-return
    ipcMain.on('stateUpdate', (event, data) => {
      if (this.conn !== null) {
        const gamepads = _.mapValues(data.gamepads, ({ axes, buttons }) => ({
          joystick_left_x: axes[0],
          joystick_left_y: axes[1],
          joystick_right_x: axes[2],
          joystick_right_y: axes[3],
          ...(_.zipObject(RuntimeClient.BUTTONS, buttons)),
        }));
        return this.conn.sendDatagram(gamepads, host);
      }
    });

    // eslint-disable-next-line consistent-return
    ipcMain.on('studentCodeStatus', (event, { studentCodeStatus }) => {
      if (this.conn !== null && this.currentCodeStatus !== studentCodeStatus) {
        this.currentCodeStatus = studentCodeStatus;

        let mode;
        switch (studentCodeStatus) {
          case robotState.TELEOP: mode = 'TELEOP'; break;
          case robotState.AUTONOMOUS: mode = 'AUTO'; break;
          case robotState.ESTOP: mode = 'ESTOP'; break;
          default: mode = 'IDLE';
        }
        console.log(`Setting mode: ${mode}`);
        return this.conn.sendCommand('set_match', [mode, null]);
      }
    });
  },
  close() {
    RendererBridge.reduxDispatch(ansibleDisconnect());
    if (this.conn !== null) {
      this.conn.closeAll();
    }
  },
};

export default Ansible;
