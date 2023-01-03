from abc import ABCMeta
from typing import Dict

from application.model.actuator.base_actuator import BaseActuator


class RotaryDiverterValveActuator(BaseActuator, metaclass=ABCMeta):

    @property
    def possible_states(self) -> Dict[str, bytes]:
        return {
            '0': b'\x00\x00\x00\x00',
            '1': b'\x00\x00\x00\x01',
            '2': b'\x00\x00\x00\x02',
            '3': b'\x00\x00\x00\x03',
            '4': b'\x00\x00\x00\x04',
            '5': b'\x00\x00\x00\x05',
        }

    @property
    def default_state(self) -> str:
        return '0'
