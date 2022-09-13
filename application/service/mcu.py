import logging
import time
from typing import Dict, List

from application.constants.mcu import IDLE, READING, EMPTY, START_RESPONSE, END_RESPONSE, GET_SNAPSHOT
from application.mcu_persistent import get_mcu
from application.mcu.measurement.base_measurement import BaseMeasurement


class MCUService:

    def __init__(self, sensor_list, measurements_list, testing=False):
        self.device_map = {device.device_id: device for device in sensor_list}
        self.measurement_map = {measurement_class(0).name: measurement_class for measurement_class in measurements_list}
        self.mcu_persistent = get_mcu()
        self.testing = testing

    def get_system_snapshot(self) -> bytes:
        if self.testing:
            # Return example response for local testing without the sensors
            return b'\xc0\x41\xd4\xb5\xf4\x42\x44\x01\x2c\x00\x00\x00\x00\xc1\x44\x47\xc0\x00\x41\xeb\xb5\x90\x42\x2a\x5a\xf0'

        self.mcu_persistent.write(GET_SNAPSHOT)
        return self.get_response()

    def get_response(self, timeout_sec=10) -> bytes:
        buffer = b''
        state = IDLE

        while True:
            byte = self.mcu_persistent.read()

            if state == IDLE:
                # Currently idling

                if byte == EMPTY:
                    # Wait so we don't keep reading nothing repeatedly
                    time.sleep(1)
                    timeout_sec -= 1
                    if timeout_sec <= 0:
                        err = f"Timeout waiting for response from MCU."
                        logging.error(err)
                        raise RuntimeError(err)

                elif byte == START_RESPONSE:
                    # Start of a new response
                    state = READING

                else:
                    # Read something unexpected
                    err = f"Unexpected response from MCU. Expected '' or '{START_RESPONSE.hex()}', but got '{byte}'"
                    logging.error(err)
                    raise RuntimeError(err)

            else:
                # Currently reading a response

                if byte == END_RESPONSE:
                    # This response is done; return it
                    return buffer

                else:
                    # Add this byte to the buffer
                    buffer += byte

    def decode_response(self, response: bytes) -> Dict[str, List[BaseMeasurement]]:
        sensor_values_map = {}

        i = 0
        while i < len(response):
            # Need to extract this one byte as a range to avoid auto casting to an int
            device_id = response[i:i+1].hex()
            i += 1

            device = self.device_map.get(device_id, None)
            if device is None:
                raise ValueError(f"Unknown device_id '{device_id}' received from MCU")

            # Read the number of floats that are returned by this device
            payload_end_i = device.payload_length * 4
            device_payload = response[i:i + payload_end_i]
            sensor_values = device.decode_payload(device_payload)

            sensor_values_map[device.sensor_name] = sensor_values
            i += payload_end_i

        return sensor_values_map

    def get_measurements(self):
        response = self.get_system_snapshot()
        sensor_values_map = self.decode_response(response)

        # Convert returned values to measurement objects
        ret = {}
        for sensor_name in sensor_values_map:
            ret[sensor_name] = []

            for measurement_name, float_val in sensor_values_map[sensor_name].items():

                measurement_class = self.measurement_map.get(measurement_name, None)
                measurement_instance = measurement_class(float_val)

                ret[sensor_name].append(measurement_instance)

        return ret
