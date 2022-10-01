from abc import ABCMeta, abstractmethod
import struct
from typing import Dict, List

from application.mcu.base_device import BaseDevice


class BaseActuator(BaseDevice, metaclass=ABCMeta):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._state = None

    @property
    def device_category(self) -> str:
        return 'actuator'

    @property
    def payload_length(self) -> int:
        return 1

    @property
    def measurement_order(self) -> List[str]:
        return ['state']

    @property
    def current_state(self):
        return self._state

    @current_state.setter
    def current_state(self, val):
        self._state = val

    @property
    @abstractmethod
    def possible_states(self) -> Dict[str, bytes]:
        pass

    @property
    @abstractmethod
    def default_state(self) -> str:
        pass

    def decode_payload(self, payload: bytes) -> Dict[str, float]:
        ret = super().decode_payload(payload)

        # Convert float values to strings
        for measurement_name in ret.keys():
            bytes_val = struct.pack('!f', ret[measurement_name])

            string_val = None
            for string_k, bytes_v in self.possible_states.items():
                if bytes_v == bytes_val:
                    string_val = string_k
                    break

            if string_val is None:
                # If we cannot get the string value for this bytes value, just set it back to a float
                string_val = ret[measurement_name]

            ret[measurement_name] = string_val

            return ret
