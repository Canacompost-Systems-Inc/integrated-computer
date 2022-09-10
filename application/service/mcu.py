import logging
import time
from typing import List

from application.mcu_persistent import get_mcu
from application.mcu.measurement.base_measurement import BaseMeasurement
from application.mcu.sensor.ds18b20_sensor import DS18B20Sensor
from application.mcu.sensor.ipc10100_sensor import IPC10100Sensor
from application.mcu.sensor.scd41_sensor import SCD41Sensor
from application.mcu.sensor.sht40_sensor import SHT40Sensor


# TODO - move this to a sensor registry? Maybe using the singleton pattern?
all_sensors = [
    SHT40Sensor(),
    SCD41Sensor(),
    IPC10100Sensor(),
    DS18B20Sensor(),
]

# TODO - move this to an API spec? or a constants file?
GET_SNAPSHOT = b'\x01\xA0\x00\x00\x00\x00\x00\x03'
GET_ACTUATOR = b'\x01\xA2\xE0\x00\x00\x00\x00\x03'
SET_ACTUATOR_HIGH = b'\x01\xB0\xE0\x11\x00\x00\x00\x03'
SET_ACTUATOR_LOW = b'\x01\xB0\xE0\x00\x00\x00\x00\x03'


class MCUService:

    def __init__(self):
        self.device_map = {device.device_id(): device for device in all_sensors}
        self.mcu_persistent = get_mcu()

    def get_system_snapshot(self) -> bytes:
        # self.mcu_persistent.write(GET_SNAPSHOT)
        # return self.get_response()
        # TODO - remove example response and instead uncomment the lines above
        # data: 'c0 41 d4 b5 f4 42 44 01 2c 00 00 00 00 c1 44 47 c0 00 41 eb b5 90 42 2a 5a f0 '
        # c0 -> device code
        # 41 d4 b5 f4 42 44 01 2c 00 00 00 00 > payload
        return b'\xc0\x41\xd4\xb5\xf4\x42\x44\x01\x2c\x00\x00\x00\x00\xc1\x44\x47\xc0\x00\x41\xeb\xb5\x90\x42\x2a\x5a\xf0'

    def get_response(self) -> bytes:
        buffer = b''
        # state machine - 0 = idle, 1 = reading response
        state = 0

        while True:
            byte = self.mcu_persistent.read()

            if state == 0:
                # Currently idling

                if byte == b'':
                    # Wait so we don't keep reading nothing repeatedly
                    time.sleep(1)

                elif byte == b'\x01':
                    # Start of a new response
                    state = 1

                else:
                    # Read something unexpected
                    logging.error(f"Unexpected response read from MCU. Expected nothing or '\x01', but got '{byte}'")
                    # TODO - raise error, or just continue on?

            else:
                # Currently reading a response

                if byte == b'\x03':
                    # This response is done; return it
                    return buffer

                else:
                    # Add this byte to the buffer
                    buffer += byte

    def decode_response(self, response: bytes) -> List[BaseMeasurement]:
        res = []

        i = 0
        while i < len(response):
            # Need to convert with to_bytes since response[i] is cast to an int
            device_id = response[i].to_bytes(1, 'big').hex()
            i += 1

            device = self.device_map.get(device_id, None)
            if device is None:
                raise ValueError(f"Unknown device_id '{device_id}' received from MCU")

            # Read the number of floats that are returned by this device
            payload_end_i = device.payload_length() * 4
            device_payload = response[i:i + payload_end_i].hex()
            res.extend(device.read_values(device_payload))
            i += payload_end_i

        return res

    def get_measurements(self):
        response = self.get_system_snapshot()
        measurements = self.decode_response(response)
        return measurements
