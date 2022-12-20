import logging
import time
from typing import Dict, List, Union

from application.constants.mcu import IDLE, READING_DEVICE_ID, READING_PAYLOAD, EMPTY, START_TRANSMISSION, \
    END_TRANSMISSION, ACKNOWLEDGE, NEGATIVE_ACKNOWLEDGE, GET_SYSTEM_SNAPSHOT_OPCODE, GET_SENSOR_STATE_OPCODE, \
    GET_ACTUATOR_STATE_OPCODE, SET_ACTUATOR_STATE_OPCODE
from application.mcu.actuator.base_actuator import BaseActuator
from application.mcu.base_device import BaseDevice
from application.mcu_persistent import get_mcu
from application.mcu.measurement.base_measurement import BaseMeasurement


class MCUService:

    def __init__(self, device_types_list, measurements_list, testing=False, device_map_config=None):

        self.device_types_map = {d().device_type_name: d for d in device_types_list}

        # Construct an object for each device in the config
        self.device_map = {}
        for location in device_map_config:
            for device_id in device_map_config[location]:
                device_type_name, device_friendly_name = device_map_config[location][device_id]

                if device_type_name not in self.device_types_map:
                    raise ValueError(f"Unknown device type name: {device_type_name} is not a sensor or actuator type")

                device_class = self.device_types_map[device_type_name]
                self.device_map[device_id] = device_class(device_id, device_friendly_name, location)

        self.measurement_map = {measurement_class(0).name: measurement_class for measurement_class in measurements_list}
        self.mcu_persistent = get_mcu()
        self.testing = testing

    def get_system_snapshot(self) -> Dict[str, Dict[str, List[BaseMeasurement]]]:
        if self.testing:
            # Return example response for local testing without the sensors
            response = b'\xc0\x41\xd5\x02\x88\x42\x48\xf6\xb9\xc1\x45\x18\x00\x00\x41\xe6\x8f\x98\x42\x33\xae\x70\xe1\x00\x00\x00\x01\xe7\x00\x00\x00\x01\xf6\x00\x00\x00\x01'
            # 41 d2 c9 c4 424b5df8c14513e00041e425a04237
        else:
            response = self._make_request(GET_SYSTEM_SNAPSHOT_OPCODE)
        #print(f"Response from get_system_snapshot: '{response.hex()}'")
        response_map = self._decode_get_response(response)
        return self.structure_response(response_map)

    def get_sensor_state(self, sensor_device_id='c0') -> Dict[str, Dict[str, List[BaseMeasurement]]]:
        if self.testing:
            # Return example response for local testing without the sensors
            response = bytes.fromhex(sensor_device_id) + b'\x41\xd5\x02\x88\x42\x48\xf6\xb9'
        else:
            response = self._make_request(GET_SENSOR_STATE_OPCODE, device_id=sensor_device_id)
        response_map = self._decode_get_response(response)
        return self.structure_response(response_map)

    def get_actuator_state(self, actuator_device_id='e0') -> Dict[str, Dict[str, List[BaseMeasurement]]]:
        if self.testing:
            # Return example response for local testing without the sensors
            response = bytes.fromhex(actuator_device_id) + b'\x00\x00\x00\x00'
        else:
            response = self._make_request(GET_ACTUATOR_STATE_OPCODE, device_id=actuator_device_id)
        response_map = self._decode_get_response(response)
        return self.structure_response(response_map)

    def set_actuator_state(self, actuator_device_id='e0', value='off') -> Dict[str, Dict[str, List[BaseMeasurement]]]:
        # Get the bytes for the payload that correspond to this value
        device: BaseActuator = self.device_map.get(actuator_device_id, None)
        if device is None:
            raise ValueError(f"Unknown device_id '{actuator_device_id}'")
        payload = device.possible_states.get(value, None)
        if payload is None:
            raise ValueError(f"Unknown value '{value}' for device {device.device_type_name}")

        if self.testing:
            # Return example response for local testing without the sensors
            response = ACKNOWLEDGE
        else:
            response = self._make_request(SET_ACTUATOR_STATE_OPCODE, device_id=actuator_device_id, payload=payload)
        response_map = self._decode_set_response(response, device_id=actuator_device_id, value=value)

        # Check for a failure
        for device_id in response_map:
            state = response_map[device_id]['state']
            if state == "UNKNOWN":
                raise RuntimeError(f"Set actuator state request failed")

        return self.structure_response(response_map)

    def _make_request(self, opcode, device_id='00', payload=b'\x00\x00\x00\x00') -> bytes:
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
                    continue
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

                device: BaseDevice = self.device_map.get(byte.hex(), None)
                if device is None:
                    raise ValueError(f"Unknown device_id '{byte.hex()}' received from MCU")

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

    def _decode_get_response(self, response: bytes) -> Dict[str, Dict[str, Union[float, str]]]:
        """
        GET Sensor Value and GET Actuator Value will return the format: <STX><DID><PAYLOAD><ETX>

        This returns a map from device_id -> {measurement_name -> value}
        """
        response_map = {}

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
            decoded_payload = device.decode_payload(payload)

            response_map[device.device_id] = decoded_payload
            i += payload_end_i

        return response_map

    def _decode_set_response(self, response: bytes, device_id: str = None, value: str = None) -> Dict[str, Dict[str, Union[float, str]]]:
        """
        SET Actuator Value will return the format: <STX><ACK><ETX> for success or <STX><NAK><ETX> for failure

        This returns a map from device_id -> {measurement_name -> value}
        Note: measurement_name is always 'state' for actuators.
        """
        response_map = {}

        # Need to extract this one byte as a range to avoid auto casting to an int
        first_byte = response[0:1]
        if first_byte == ACKNOWLEDGE:
            # Set the state to the intended value
            state = value
        elif first_byte == NEGATIVE_ACKNOWLEDGE:
            logging.error(f"MCU reported a failure to set the actuator state for device {device_id}")
            # Return an UNKNOWN state so the calling function can log the error
            state = 'UNKNOWN'
        else:
            raise ValueError(f"Unknown response to set actuator value '{first_byte}' received from MCU")

        device: BaseDevice = self.device_map.get(device_id, None)
        response_map[device.device_id] = {'state': state}
        return response_map

    def structure_response(self, response_map) -> Dict[str, Dict[str, List[BaseMeasurement]]]:
        # Convert returned values to measurement objects

        # Response is structured like the device map in the config. i.e.
        # {location -> {device_id -> (device_friendly_name, [measurements])}}
        ret = {}

        for device_id in response_map:

            device: BaseDevice = self.device_map.get(device_id, None)

            if device.location not in ret:
                ret[device.location] = {}

            ret[device.location][device.device_id] = (device.device_friendly_name, [])

            for measurement_name, float_val in response_map[device_id].items():

                measurement_class = self.measurement_map.get(measurement_name, None)
                measurement_instance = measurement_class(float_val)

                ret[device.location][device.device_id][1].append(measurement_instance)

        return ret
