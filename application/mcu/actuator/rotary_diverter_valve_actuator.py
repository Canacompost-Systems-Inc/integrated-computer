from abc import ABCMeta
from typing import Dict

from application.mcu.actuator.base_actuator import BaseActuator


class RotaryDiverterValveActuator(BaseActuator, metaclass=ABCMeta):

    @property
    def possible_states(self) -> Dict[str, bytes]:
        return {
            'ref': b'\x00\x00\x00\x00',
            '0': b'\x00\x00\x00\x01',
            '1': b'\x00\x00\x00\x02',
            '2': b'\x00\x00\x00\x03',
            '3': b'\x00\x00\x00\x04',
            '4': b'\x00\x00\x00\x05',
            '5': b'\x00\x00\x00\x06',
        }

    @property
    def default_state(self) -> str:
        return '0'
