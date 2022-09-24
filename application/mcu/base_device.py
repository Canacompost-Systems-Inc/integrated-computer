from abc import ABCMeta, abstractmethod
import struct
from typing import Dict, List


class BaseDevice(metaclass=ABCMeta):

    def __init__(self, device_id=None, device_friendly_name=None, location=None):
        self.device_id = device_id
        self.device_friendly_name = device_friendly_name
        self.location = location

    @property
    @abstractmethod
    def device_category(self) -> str:
        """
        Property denoting the device category. Either 'sensor' or 'actuator'.
        """
        pass

    @property
    @abstractmethod
    def device_type_name(self) -> str:
        pass

    @property
    @abstractmethod
    def payload_length(self) -> int:
        pass

    @property
    @abstractmethod
    def measurement_order(self) -> List[str]:
        pass

    def decode_payload(self, payload: bytes) -> Dict[str, float]:
        """
        Function to take the device payload as bytes and return a map from measurement_name to float value. An actuator
        will return just one measurement_name 'state'.
        """
        ret = {}
        for i in range(self.payload_length):
            if i >= len(self.measurement_order):
                break
            bytes_val = payload[i*4:i*4+4]
            float_val = struct.unpack('!f', bytes_val)[0]
            measurement_name = self.measurement_order[i]
            ret[measurement_name] = float_val
        return ret
