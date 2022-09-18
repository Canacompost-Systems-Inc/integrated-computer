import logging
import time
from typing import Dict, List

from application.constants.mcu import IDLE, READING, EMPTY, START_TRANSMISSION, END_TRANSMISSION, \
    ACKNOWLEDGE, NEGATIVE_ACKNOWLEDGE, GET_SYSTEM_SNAPSHOT_OPCODE, GET_SENSOR_STATE_OPCODE, GET_ACTUATOR_STATE_OPCODE,\
    SET_ACTUATOR_STATE_OPCODE, SET_ACTUATOR_STATE_PAYLOAD_LOW, SET_ACTUATOR_STATE_PAYLOAD_HIGH
from application.mcu_persistent import get_mcu
from application.mcu.measurement.base_measurement import BaseMeasurement


class MCUService:

    def __init__(self, sensor_list, measurements_list, testing=False):
        self.device_map = {device.device_id: device for device in sensor_list}
        self.measurement_map = {measurement_class(0).name: measurement_class for measurement_class in measurements_list}
        self.mcu_persistent = get_mcu()
        self.testing = testing

    def get_system_snapshot(self) -> Dict[str, List[BaseMeasurement]]:
        if self.testing:
            # Return example response for local testing without the sensors
            response = b'\xc0\x41\xd4\xb5\xf4\x42\x44\x01\x2c\x00\x00\x00\x00\xc1\x44\x47\xc0\x00\x41\xeb\xb5\x90\x42\x2a\x5a\xf0'
        else:
            response = self.make_request(GET_SYSTEM_SNAPSHOT_OPCODE)
        response_map = self.decode_response(response)
        return self.convert_response_map_to_measurements(response_map)

    def get_sensor_state(self, sensor_device_id=b'\xC0') -> Dict[str, List[BaseMeasurement]]:
        response = self.make_request(GET_SENSOR_STATE_OPCODE, device_id=sensor_device_id)
        response_map = self.decode_response(response)
        return self.convert_response_map_to_measurements(response_map)

    def get_actuator_state(self, actuator_device_id=b'\xE0') -> Dict[str, Dict[str, float]]:
        response = self.make_request(GET_ACTUATOR_STATE_OPCODE, device_id=actuator_device_id)
        response_map = self.decode_response(response)
        # TODO - need a function to convert the response map to actuator states
        return response_map

    def set_actuator_state(self, actuator_device_id=b'\xE0', value='low') -> bool:
        if value == 'low':
            payload = SET_ACTUATOR_STATE_PAYLOAD_LOW
        elif value == 'high':
            payload = SET_ACTUATOR_STATE_PAYLOAD_HIGH
        else:
            raise ValueError(f"Unknown value for setting actuator state; must be 'low' or 'high', not '{value}'")
        response = self.make_request(SET_ACTUATOR_STATE_OPCODE, device_id=actuator_device_id, payload=payload)
        response_map = self.decode_response(response)
        if not bool(response_map['status']['status']):
            # The set request failed
            raise RuntimeError(f"Set actuator state request failed")
        return True

    def make_request(self, opcode, device_id=b'\x00', payload=b'\x00\x00\x00\x00') -> bytes:
        request = START_TRANSMISSION + opcode + device_id + payload + END_TRANSMISSION
        self.mcu_persistent.write(request)
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

                elif byte == START_TRANSMISSION:
                    # Start of a new response
                    state = READING

                else:
                    # Read something unexpected
                    err = f"Unexpected response from MCU. Expected '' or '{START_TRANSMISSION.hex()}', but got '{byte}'"
                    logging.error(err)
                    raise RuntimeError(err)

            else:
                # Currently reading a response

                if byte == END_TRANSMISSION:
                    # This response is done; return it
                    break

                else:
                    # Add this byte to the buffer
                    buffer += byte

        return buffer

    def decode_response(self, response: bytes) -> Dict[str, Dict[str, float]]:
        """
        GET Sensor Value and GET Actuator Value will return the format: <STX><DID><PAYLOAD><ETX>
        SET Actuator Value will return the format: <STX><ACK><ETX> for success or <STX><NAK><ETX> for failure
        """
        response_map = {}

        i = 0
        while i < len(response):
            # Need to extract this one byte as a range to avoid auto casting to an int
            first_byte = response[i:i+1].hex()

            # If this returns ACK or NAK, that is the entire message so just return
            if first_byte == ACKNOWLEDGE:
                response_map['status'] = {}
                response_map['status']['status'] = float(True)
                break
            elif first_byte == NEGATIVE_ACKNOWLEDGE:
                response_map['status'] = {}
                response_map['status']['status'] = float(False)
                break

            device_id = response[i:i+1].hex()
            i += 1

            device = self.device_map.get(device_id, None)
            if device is None:
                raise ValueError(f"Unknown device_id '{device_id}' received from MCU")

            # Read the number of floats that are returned by this device
            payload_end_i = device.payload_length * 4
            device_payload = response[i:i + payload_end_i]
            sensor_values = device.decode_payload(device_payload)

            response_map[device.sensor_name] = sensor_values
            i += payload_end_i

        return response_map

    def convert_response_map_to_measurements(self, response_map) -> Dict[str, List[BaseMeasurement]]:
        # Convert returned values to measurement objects
        ret = {}
        for sensor_name in response_map:
            ret[sensor_name] = []

            for measurement_name, float_val in response_map[sensor_name].items():

                measurement_class = self.measurement_map.get(measurement_name, None)
                measurement_instance = measurement_class(float_val)

                ret[sensor_name].append(measurement_instance)

        return ret
