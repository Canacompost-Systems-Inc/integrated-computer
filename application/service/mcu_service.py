import logging
import time
from typing import Dict, List

from application.constants.mcu import IDLE, READING_DEVICE_ID, READING_PAYLOAD, EMPTY, START_TRANSMISSION, \
    END_TRANSMISSION, ACKNOWLEDGE, NEGATIVE_ACKNOWLEDGE, GET_SYSTEM_SNAPSHOT_OPCODE, GET_SENSOR_STATE_OPCODE, \
    GET_ACTUATOR_STATE_OPCODE, SET_ACTUATOR_STATE_OPCODE
from application.model.actuator.base_actuator import BaseActuator
from application.model.base_device import BaseDevice
from application.model.datum import Datum
from application.persistence.mcu_persistent import get_mcu


class MCUService:

    def __init__(self, device_types_list, measurements_list, device_map_config=None, testing=False):

        self.mcu_persistent = get_mcu()

        self.device_types_map = {d().device_type_name: d for d in device_types_list}

        # Construct an object for each device in the config
        self.device_map = {}
        for location in device_map_config:
            for device_id in device_map_config[location]:
                device_type_name, device_friendly_name = device_map_config[location][device_id]

                if device_type_name not in self.device_types_map:
                    raise ValueError(f"Unknown device type name: {device_type_name} is not a sensor or actuator type")

                device_class = self.device_types_map[device_type_name]
                device_instance = device_class(device_id, device_friendly_name, location)
                self.device_map[device_id] = device_instance

        self.measurement_class_map = {measurement_class(0).name: measurement_class for measurement_class in measurements_list}

        self.testing = testing

    def get_system_snapshot(self) -> Dict[str, List[Datum]]:
        response = self.make_request(GET_SYSTEM_SNAPSHOT_OPCODE)
        return self.decode_get_response(response)

    def get_sensor_state(self, sensor_device_id='c0') -> Dict[str, List[Datum]]:
        response = self.make_request(GET_SENSOR_STATE_OPCODE, device_id=sensor_device_id)
        return self.decode_get_response(response)

    def get_actuator_state(self, actuator_device_id='e0') -> Dict[str, List[Datum]]:
        response = self.make_request(GET_ACTUATOR_STATE_OPCODE, device_id=actuator_device_id)
        return self.decode_get_response(response)

    def set_actuator_state(self, actuator_device_id='e0', value='off') -> Dict[str, List[Datum]]:

        def get_payload_bytes(_value):
            """Get the bytes for the payload that correspond to this value"""
            device: BaseActuator = self.device_map.get(actuator_device_id, None)
            if device is None:
                raise ValueError(f"Unknown device_id '{actuator_device_id}'")
            _payload = device.possible_states.get(_value, None)
            if _payload is None:
                raise ValueError(f"Unknown value '{_value}' for device {device.device_type_name}")
            return _payload

        def decode_set_response(_response: bytes) -> Dict[str, List[Datum]]:
            ret = {actuator_device_id: []}

            device: BaseActuator = self.device_map.get(actuator_device_id, None)
            if device is None:
                raise ValueError(f"Unknown device_id '{actuator_device_id}'")

            measurement_class = self.measurement_class_map.get("state")

            """Need to extract this one byte as a range to avoid auto casting to an int"""
            response_byte = _response[0:1]

            if response_byte == ACKNOWLEDGE:
                pass

            elif response_byte == NEGATIVE_ACKNOWLEDGE:
                err = f"MCU reported a failure to set the actuator state for device {actuator_device_id}"
                logging.error(err)
                raise RuntimeError(err)

            else:
                raise ValueError(f"Unknown response to set actuator state '{response_byte}' received from MCU")

            measurement = measurement_class(value)
            dat = Datum(device, measurement)
            ret[actuator_device_id].append(dat)
            return ret

        payload = get_payload_bytes(value)
        response = self.make_request(SET_ACTUATOR_STATE_OPCODE, device_id=actuator_device_id, payload=payload)
        return decode_set_response(response)

    def decode_get_response(self, response: bytes) -> Dict[str, List[Datum]]:
        ret = {}

        device_payloads = self.split_response_by_device_id(response)

        for device_id, payload_bytes in device_payloads.items():

            device: BaseDevice = self.device_map.get(device_id, None)
            if device is None:
                raise ValueError(f"Unknown device_id '{device_id}' received from MCU")

            measurement_name_to_value_map = device.decode_payload(payload_bytes)

            ret[device_id] = []
            for measurement_name, value in measurement_name_to_value_map.items():
                
                measurement_class = self.measurement_class_map.get(measurement_name, None)
                if measurement_class is None:
                    raise ValueError(f"Unknown measurement_name '{measurement_name}' for device '{device_id}'")

                measurement = measurement_class(value)
                
                dat = Datum(device, measurement)
                ret[device_id].append(dat)

        return ret

    def make_request(self, opcode, device_id='00', payload=b'\x00\x00\x00\x00') -> bytes:

        # If we are testing, there is no MCU to make requests to or read responses from, so return example responses
        if self.testing:
            if opcode == GET_SYSTEM_SNAPSHOT_OPCODE:
                response = b'\xc0\x41\xd5\x02\x88\x42\x48\xf6\xb9\xc1\x45\x18\x00\x00\x41\xe6\x8f\x98\x42\x33\xae\x70\xe1\x00\x00\x00\x01\xe7\x00\x00\x00\x01\xf6\x00\x00\x00\x01'
            elif opcode == GET_SENSOR_STATE_OPCODE:
                response = bytes.fromhex(device_id) + b'\x41\xd5\x02\x88\x42\x48\xf6\xb9'
            elif opcode == GET_ACTUATOR_STATE_OPCODE:
                response = bytes.fromhex(device_id) + b'\x00\x00\x00\x00'
            elif opcode == SET_ACTUATOR_STATE_OPCODE:
                response = ACKNOWLEDGE
            else:
                raise RuntimeError(f"Unknown opcode '{opcode}'")
            return response

        request = START_TRANSMISSION + opcode + bytes.fromhex(device_id) + payload + END_TRANSMISSION
        self.mcu_persistent.write(request)
        return self._get_response()

    def _get_response(self, timeout_sec=10) -> bytes:
        buffer = b''
        state = IDLE
        current_payload_length = 0

        while True:

            byte = self.mcu_persistent.read()

            if byte == EMPTY:
                # Wait so we don't keep reading nothing repeatedly
                time.sleep(1)
                timeout_sec -= 1
                if timeout_sec <= 0:
                    err = f"Timeout waiting for response from MCU."
                    logging.error(err)
                    raise RuntimeError(err)
                continue

            if state == IDLE:
                # Currently idling, waiting for start transmission byte

                if byte == START_TRANSMISSION:
                    # Start of a new response
                    state = READING_DEVICE_ID

                else:
                    # Read something unexpected
                    err = f"Unexpected response from MCU. Expected '' or '{START_TRANSMISSION.hex()}', but got '{byte.hex()}'"
                    logging.error(err)
                    raise RuntimeError(err)

            elif state == READING_DEVICE_ID:
                # Reading the one-byte device id

                if byte == END_TRANSMISSION:
                    # This response is done; return it since we're done
                    break

                # Add this byte to the buffer
                buffer += byte

                # If this is a set response, we won't get a device id (just an ACK or NAK)
                if byte == ACKNOWLEDGE or byte == NEGATIVE_ACKNOWLEDGE:
                    continue

                device_id = byte.hex()

                device: BaseDevice = self.device_map.get(device_id, None)
                if device is None:
                    raise ValueError(f"Unknown device_id '{device_id}' received from MCU")

                current_payload_length = device.payload_length * 4

                state = READING_PAYLOAD

            elif state == READING_PAYLOAD:
                # Reading the payload

                # Add this byte to the buffer
                buffer += byte

                # Continue reading until bytes from this payload are consumed
                current_payload_length -= 1
                if current_payload_length > 0:
                    continue

                # Done reading payload, return to checking for device id or end transmission char
                state = READING_DEVICE_ID

        return buffer

    def split_response_by_device_id(self, response: bytes) -> Dict[str, bytes]:
        """
        GET Sensor Value and GET Actuator Value will return the format: <STX><DID><PAYLOAD><ETX>

        This returns a map from device_id -> payload_bytes so that this response can be decoded
        """
        payload_map = {}

        i = 0
        while i < len(response):
            # Need to extract this one byte as a range to avoid auto casting to an int
            device_id = response[i:i+1].hex()
            i += 1

            device: BaseDevice = self.device_map.get(device_id, None)
            if device is None:
                raise ValueError(f"Unknown device_id '{device_id}' received from MCU")

            # Read the number of floats that are returned by this device
            payload_end_i = device.payload_length * 4
            payload = response[i:i + payload_end_i]

            payload_map[device_id] = payload
            i += payload_end_i

        return payload_map
