from abc import ABC, abstractmethod
from typing import Dict, List
import struct


class BaseSensor(ABC):

    @property
    @abstractmethod
    def sensor_name(self) -> str:
        pass

    @property
    @abstractmethod
    def device_id(self) -> str:
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
        Function to take the device payload as bytes and return a map from measurement_name to float value
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
