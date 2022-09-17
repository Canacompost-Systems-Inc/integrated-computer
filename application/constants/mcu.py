
# State machine for reading values from MCU
IDLE = 0
READING = 1

# Byte values read from MCU
EMPTY = b''
START_RESPONSE = b'\x01'
END_RESPONSE = b'\x03'

# Bytes for requests to MCU
GET_SNAPSHOT = b'\x01\xA0\x00\x00\x00\x00\x00\x03'
GET_ACTUATOR = b'\x01\xA2\xE0\x00\x00\x00\x00\x03'
SET_ACTUATOR_HIGH = b'\x01\xB0\xE0\x11\x00\x00\x00\x03'
SET_ACTUATOR_LOW = b'\x01\xB0\xE0\x00\x00\x00\x00\x03'
