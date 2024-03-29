import logging
import time
from typing import Dict, List, Optional

from application.constants.mcu import IDLE, READING_DEVICE_ID, READING_PAYLOAD, EMPTY, START_TRANSMISSION, \
    END_TRANSMISSION, ACKNOWLEDGE, NEGATIVE_ACKNOWLEDGE, GET_SYSTEM_SNAPSHOT_OPCODE, GET_SENSOR_STATE_OPCODE, \
    GET_ACTUATOR_STATE_OPCODE, SET_ACTUATOR_STATE_OPCODE
from application.model.datum import Datum
from application.persistence.mcu_persistent import get_mcu
from application.service.device_registry_service import DeviceRegistryService
from application.service.measurement_factory import MeasurementFactory


class MCUService:

    def __init__(self, device_registry_service: DeviceRegistryService, measurement_factory: MeasurementFactory,
                 testing=False, demo_mode=False, disabled_devices: Optional[List] = None):

        if disabled_devices is None:
            disabled_devices = []

        self.device_registry_service = device_registry_service
        self.measurement_factory = measurement_factory
        self.testing = testing
        self.demo_mode = demo_mode
        self.disabled_devices = disabled_devices

        self.mcu_persistent = get_mcu()

    def get_system_snapshot(self) -> Dict[str, List[Datum]]:
        self.clear_buffers()
        response = self._make_request(GET_SYSTEM_SNAPSHOT_OPCODE)
        return self._decode_get_response(response)

    def get_sensor_state(self, sensor_device_id='c0') -> Dict[str, List[Datum]]:
        if sensor_device_id in self.disabled_devices:
            logging.debug(f"Skipping because this device is disabled")
            return {}
        self.clear_buffers()
        response = self._make_request(GET_SENSOR_STATE_OPCODE, device_id=sensor_device_id)
        return self._decode_get_response(response)

    def get_actuator_state(self, actuator_device_id='e0') -> Dict[str, List[Datum]]:
        if actuator_device_id in self.disabled_devices:
            logging.debug(f"Skipping because this device is disabled")
            return {}
        self.clear_buffers()
        response = self._make_request(GET_ACTUATOR_STATE_OPCODE, device_id=actuator_device_id)
        return self._decode_get_response(response)

    def set_actuator_state(self, actuator_device_id='e0', value='off') -> Dict[str, List[Datum]]:
        if actuator_device_id in self.disabled_devices:
            logging.debug(f"Skipping because this device is disabled")
            return {}

        def _decode_set_response(_response: bytes) -> Dict[str, List[Datum]]:
            """
            SET Actuator Value will return the format: <STX><ACK><ETX> for success or <STX><NAK><ETX> for failure
            
            This returns a map from device_id -> [Datum objects for this device]
            Note: this format is returned so all MCU endpoints returns the same object structure
            Note: measurement_name is always 'state' for actuators
            """

            # Need to extract this one byte as a range to avoid auto casting to an int
            response_byte = _response[0:1]

            if response_byte == ACKNOWLEDGE:
                pass

            elif response_byte == NEGATIVE_ACKNOWLEDGE:
                err = f"MCU reported a failure to set the actuator state for device {actuator_device_id}"
                logging.error(err)
                raise RuntimeError(err)

            else:
                raise ValueError(f"Unknown response to set actuator state '{response_byte}' received from MCU")

            # Create datum for this state measurement
            device = self.device_registry_service.get_device(actuator_device_id)
            measurement = self.measurement_factory.get_measurement('state', value)
            dat = Datum(device, measurement)

            # Return the expected data structure
            return {actuator_device_id: [dat]}

        payload = self.device_registry_service.get_payload_bytes(actuator_device_id, value)
        self.clear_buffers()
        response = self._make_request(SET_ACTUATOR_STATE_OPCODE, device_id=actuator_device_id, payload=payload)
        return _decode_set_response(response)

    def clear_buffers(self):
        # Get the contents of the input buffer
        buffer = b''
        if self.mcu_persistent is None:
            return
        if self.mcu_persistent.in_waiting == 0:
            return
        # Give it time to receive the rest of the input
        time.sleep(1)
        try:
            buffer = self.mcu_persistent.read(self.mcu_persistent.in_waiting)
        except Exception as e:
            logging.debug(f"Encountered error while reading input buffer: {e}")
        # Print the contents of the input buffer
        if buffer != b'':
            logging.debug(f"Buffer contents: {buffer}")
            try:
                decoded = bytes.fromhex(buffer).decode('utf-8')
                logging.debug(f"Response from MCU (decoded): {decoded}")
            except Exception:
                pass
        # Clear the buffers
        self.mcu_persistent.reset_input_buffer()
        self.mcu_persistent.reset_output_buffer()
        # Give it time before continuing to use the connection
        time.sleep(1)

    def _decode_get_response(self, response: bytes) -> Dict[str, List[Datum]]:
        """
        GET Sensor Value and GET Actuator Value will return the format: <STX><DID><PAYLOAD><ETX>
        This format is repeated for each device (which only applies to the GET System Snapshot endpoint)

        This returns a map from device_id -> [Datum objects for this device]
        """

        ret = {}

        # Check for failure
        # Need to extract this one byte as a range to avoid auto casting to an int
        response_byte = response[0:1]
        if response_byte == NEGATIVE_ACKNOWLEDGE:
            err = f"MCU reported a failure when performing the get response"
            logging.error(err)
            raise RuntimeError(err)

        device_payloads = self._split_response_by_device_id(response)

        for device_id, payload_bytes in device_payloads.items():

            device = self.device_registry_service.get_device(device_id)
            measurement_name_to_value_map = device.decode_payload(payload_bytes)

            ret[device_id] = []
            for measurement_name, value in measurement_name_to_value_map.items():
                
                device = self.device_registry_service.get_device(device_id)
                measurement = self.measurement_factory.get_measurement(measurement_name, value)
                dat = Datum(device, measurement)
                ret[device_id].append(dat)

        return ret

    def _make_request(self, opcode, device_id='00', payload=b'\x00\x00\x00\x00') -> bytes:

        # If we are testing, there is no MCU to make requests to or read responses from, so return example responses
        if self.testing:
            if opcode == GET_SYSTEM_SNAPSHOT_OPCODE:
                response = b'\xc1\x43\xf8\x80\x00\x41\xbf\x88\x30\x41\xfe\x23\x60\xc2\xc2\x30\x7f\x20\x47\xf3\x97\x1a\xc7\x00\x00\x00\x00\xe0\x00\x00\x00\x00\xe1\x00\x00\x00\x01\xe2\x00\x00\x00\x00\xe3\x00\x00\x00\x00\xe4\x00\x00\x00\x00\xe5\x00\x00\x00\x00\xe6\x00\x00\x00\x00\xe7\x00\x00\x00\x00\xe8\x00\x00\x00\x00\xeb\x00\x00\x00\x00\xec\x00\x00\x00\x00\xf0\x00\x00\x00\x00\xe9\x00\x00\x00\x00\xf6\x00\x00\x00\x00\xf8\x00\x00\x00\x00\xfa\x00\x00\x00\x00\xf1\x00\x00\x00\x00\xf2\x00\x00\x00\x00\xf3\x00\x00\x00\x00\xf4\x00\x00\x00\x00'

            elif opcode == GET_SENSOR_STATE_OPCODE:
                # Example responses:
                # response = b'\xc1\x44\x0d\xc0\x00\x41\xb8\x4f\xc0\x41\xc4\x1b\x20'
                # response = b'\xc2\xc2\x30\x7f\x20\x47\xf3\x97\x1a'

                # Construct a response that is within the acceptable range
                response = bytes.fromhex(device_id)

                for measurement_name in self.device_registry_service.get_device(device_id).measurement_order:

                    measurement = self.measurement_factory.get_measurement(measurement_name, 0)
                    range_min = max(measurement.normal_min, measurement.ideal_min)
                    range_max = min(measurement.normal_max, measurement.ideal_max)

                    from random import uniform
                    random_value = uniform(range_min, range_max)

                    # Add this measurement to the response
                    import struct
                    response += struct.pack("!f", random_value)

            elif opcode == GET_ACTUATOR_STATE_OPCODE:
                # Example responses:
                # response = b'\xe0\x00\x00\x00\x00'
                # response = b'\xeb\x00\x00\x00\x00'

                # Construct a response from the possible states
                response = bytes.fromhex(device_id)
                possible_states = self.device_registry_service.get_device(device_id).possible_states

                from random import choice
                random_value_bytes = choice(list(possible_states.values()))

                response += random_value_bytes

            elif opcode == SET_ACTUATOR_STATE_OPCODE:
                response = ACKNOWLEDGE

            else:
                raise RuntimeError(f"Unknown opcode '{opcode}'")

            return response

        # If demo mode is enabled, we need to retry multiple times since the MCU will write errors occasionally
        if self.demo_mode:
            request = START_TRANSMISSION + opcode + bytes.fromhex(device_id) + payload + END_TRANSMISSION

            # Retry this many times (plus one more down below)
            for _ in range(3):

                self.mcu_persistent.write(request)
                _response = None
                try:
                    _response = self._get_response()
                except RuntimeError as e:
                    # If we got a timeout, continue raising the error since we're screwed
                    if 'Timeout waiting for response from MCU' in str(e):
                        raise e
                    # Otherwise, just try writing the request again
                    continue
                if _response is not None:
                    break

            # If this is a get measurement call, the sensor may not be working so get fake data in the expected range
            if opcode == GET_SENSOR_STATE_OPCODE and _response == NEGATIVE_ACKNOWLEDGE:

                # Construct a response that is within the acceptable range
                response = bytes.fromhex(device_id)

                for measurement_name in self.device_registry_service.get_device(device_id).measurement_order:

                    from application.constants.demo import MEASUREMENT_RANGES
                    range_min = MEASUREMENT_RANGES.get(measurement_name, (0.0, 0.0))[0]
                    range_max = MEASUREMENT_RANGES.get(measurement_name, (0.0, 0.0))[1]

                    from random import uniform
                    random_value = uniform(range_min, range_max)

                    # Add this measurement to the response
                    import struct
                    response += struct.pack("!f", random_value)

                return response

            return _response

        request = START_TRANSMISSION + opcode + bytes.fromhex(device_id) + payload + END_TRANSMISSION
        # logging.debug(f"Writing to MCU: {request.hex()}")
        self.mcu_persistent.write(request)
        return self._get_response()

    def _get_response(self, timeout_sec=10) -> bytes:
        # logging.debug(f"Getting response from MCU")
        buffer = b''
        state = IDLE
        current_payload_length_bytes = 0

        while True:

            byte = self.mcu_persistent.read()

            # logging.debug(f"Received byte from MCU: {byte.hex()}")

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
                    # Read something unexpected - clear the buffer then raise error
                    err = f"Unexpected response from MCU. Expected '' or '{START_TRANSMISSION.hex()}', but got '{byte.hex()}'"
                    logging.error(err)
                    self.clear_buffers()
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

                device_payload_length = self.device_registry_service.get_payload_length(device_id)
                current_payload_length_bytes = device_payload_length * 4

                state = READING_PAYLOAD

            elif state == READING_PAYLOAD:
                # Reading the payload

                # Add this byte to the buffer
                buffer += byte

                # Continue reading until bytes from this payload are consumed
                current_payload_length_bytes -= 1
                if current_payload_length_bytes > 0:
                    continue

                # Done reading payload, return to checking for device id or end transmission char
                state = READING_DEVICE_ID

        logging.debug(f"Response from MCU: {buffer.hex()}")

        return buffer

    def _split_response_by_device_id(self, response: bytes) -> Dict[str, bytes]:
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

            # Read the number of floats that are returned by this device
            device_payload_length = self.device_registry_service.get_payload_length(device_id)
            payload_end_i = device_payload_length * 4
            payload = response[i:i + payload_end_i]

            payload_map[device_id] = payload
            i += payload_end_i

        return payload_map
