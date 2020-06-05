# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: notification.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='notification.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=b'\n\x12notification.proto\"\xc8\x03\n\x0cNotification\x12\"\n\x06header\x18\x01 \x01(\x0e\x32\x12.Notification.Type\x12\x16\n\x0e\x63onsole_output\x18\x02 \x01(\t\x12\x33\n\x0esensor_mapping\x18\x03 \x03(\x0b\x32\x1b.Notification.SensorMapping\x12\x12\n\ntimestamps\x18\x04 \x03(\x01\x12\x1a\n\x12gamecode_solutions\x18\x05 \x03(\x05\x12\x11\n\tgamecodes\x18\x06 \x03(\x05\x12\r\n\x05rfids\x18\x07 \x03(\x05\x1a@\n\rSensorMapping\x12\x12\n\ndevice_uid\x18\x01 \x01(\t\x12\x1b\n\x13\x64\x65vice_student_name\x18\x02 \x01(\t\"\xb2\x01\n\x04Type\x12\x13\n\x0f\x43ONSOLE_LOGGING\x10\x00\x12\x10\n\x0cSTUDENT_SENT\x10\x01\x12\x14\n\x10STUDENT_RECEIVED\x10\x02\x12\x18\n\x14STUDENT_NOT_RECEIVED\x10\x03\x12\x12\n\x0eSENSOR_MAPPING\x10\x04\x12\x10\n\x0cTIMESTAMP_UP\x10\x05\x12\x12\n\x0eTIMESTAMP_DOWN\x10\x06\x12\x19\n\x15GAMECODE_TRANSMISSION\x10\x07\x62\x06proto3'
)



_NOTIFICATION_TYPE = _descriptor.EnumDescriptor(
  name='Type',
  full_name='Notification.Type',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='CONSOLE_LOGGING', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='STUDENT_SENT', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='STUDENT_RECEIVED', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='STUDENT_NOT_RECEIVED', index=3, number=3,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SENSOR_MAPPING', index=4, number=4,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='TIMESTAMP_UP', index=5, number=5,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='TIMESTAMP_DOWN', index=6, number=6,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='GAMECODE_TRANSMISSION', index=7, number=7,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=301,
  serialized_end=479,
)
_sym_db.RegisterEnumDescriptor(_NOTIFICATION_TYPE)


_NOTIFICATION_SENSORMAPPING = _descriptor.Descriptor(
  name='SensorMapping',
  full_name='Notification.SensorMapping',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='device_uid', full_name='Notification.SensorMapping.device_uid', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='device_student_name', full_name='Notification.SensorMapping.device_student_name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=234,
  serialized_end=298,
)

_NOTIFICATION = _descriptor.Descriptor(
  name='Notification',
  full_name='Notification',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='header', full_name='Notification.header', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='console_output', full_name='Notification.console_output', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='sensor_mapping', full_name='Notification.sensor_mapping', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='timestamps', full_name='Notification.timestamps', index=3,
      number=4, type=1, cpp_type=5, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='gamecode_solutions', full_name='Notification.gamecode_solutions', index=4,
      number=5, type=5, cpp_type=1, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='gamecodes', full_name='Notification.gamecodes', index=5,
      number=6, type=5, cpp_type=1, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='rfids', full_name='Notification.rfids', index=6,
      number=7, type=5, cpp_type=1, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_NOTIFICATION_SENSORMAPPING, ],
  enum_types=[
    _NOTIFICATION_TYPE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=23,
  serialized_end=479,
)

_NOTIFICATION_SENSORMAPPING.containing_type = _NOTIFICATION
_NOTIFICATION.fields_by_name['header'].enum_type = _NOTIFICATION_TYPE
_NOTIFICATION.fields_by_name['sensor_mapping'].message_type = _NOTIFICATION_SENSORMAPPING
_NOTIFICATION_TYPE.containing_type = _NOTIFICATION
DESCRIPTOR.message_types_by_name['Notification'] = _NOTIFICATION
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Notification = _reflection.GeneratedProtocolMessageType('Notification', (_message.Message,), {

  'SensorMapping' : _reflection.GeneratedProtocolMessageType('SensorMapping', (_message.Message,), {
    'DESCRIPTOR' : _NOTIFICATION_SENSORMAPPING,
    '__module__' : 'notification_pb2'
    # @@protoc_insertion_point(class_scope:Notification.SensorMapping)
    })
  ,
  'DESCRIPTOR' : _NOTIFICATION,
  '__module__' : 'notification_pb2'
  # @@protoc_insertion_point(class_scope:Notification)
  })
_sym_db.RegisterMessage(Notification)
_sym_db.RegisterMessage(Notification.SensorMapping)


# @@protoc_insertion_point(module_scope)