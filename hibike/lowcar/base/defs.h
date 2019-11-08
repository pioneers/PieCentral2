#ifndef DEFS_H
#define DEFS_H

#include "Arduino.h"
#include <stdint.h>

// Analog Input Pins (not sure if we need)
#define IO0 A0
#define IO1 A1
#define IO2 A2
#define IO3 A3

// Digital Input Pins (not sure if we need)
#define IO4 2
#define IO5 3
#define IO6 6
#define IO7 9
#define IO8 10
#define IO9 11

#define LED_PIN 13

//message ID enumerations
enum class MessageID {
  PING                    = 0x00,
  SUBSCRIPTION_REQUEST    = 0x01,
  SUBSCRIPTION_RESPONSE   = 0x02,
  DEVICE_READ             = 0x03,
  DEVICE_WRITE            = 0x04,
  DEVICE_DATA             = 0x05,
  DEVICE_DISABLE          = 0x06,
  HEARTBEAT_REQUEST      = 0x07,
  HEARTBEAT_RESPONSE     = 0x08,

  ERROR                   = 0xFF,
};

//identification for device types
enum class DeviceID {
  LIMIT_SWITCH = 0x00,
  POLAR_BEAR = 0x01
  LINE_FOLLOWER = 0x02,
  BATTERY_BUZZER = 0x03,
  TEAM_FLAG = 0x04,
  RFID = 0x05,
  SERVO_CONTROL = 0x06,
  COLOR_SENSOR = 0x07,
  EXAMPLE_DEVICE = 0xFF
};

//decoded lowcar packet
typedef struct _message {
  uint8_t message_id;
  uint8_t payload_length;
  uint8_t payload[MAX_PAYLOAD_SIZE];
} message_t;

//unique id struct for a specific device
typedef struct _uid {
  uint16_t device_type;
  uint8_t year;
  uint64_t id;
} uid_t;

#endif