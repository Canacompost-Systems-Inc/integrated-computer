from abc import ABC, abstractmethod
from typing import List
import struct

from application.mcu.measurement.base_measurement import BaseMeasurement


class BaseSensor(ABC):

    @property
    @abstractmethod
    def device_id(self) -> bytes:
        pass

    @property
    @abstractmethod
    def payload_length(self) -> int:
        pass

    @abstractmethod
    def read_values(self, payload: bytes) -> List[BaseMeasurement]:
        pass

    def decode_payload(self, payload: str) -> List[float]:
        ret = []
        for i in range(self.payload_length()):
            bytes_val = payload[i*8:i*8+8]
            val = struct.unpack('!f', bytes.fromhex(bytes_val))[0]
            ret.append(val)
        return ret
