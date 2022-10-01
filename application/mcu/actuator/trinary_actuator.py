from abc import ABCMeta
from typing import Dict

from application.mcu.actuator.base_actuator import BaseActuator


class TrinaryActuator(BaseActuator, metaclass=ABCMeta):

    @property
    def possible_states(self) -> Dict[str, bytes]:
        return {
            '0': b'\x00\x00\x00\x00',
            '1': b'\x11\x11\x11\x11',
            '2': b'\x22\x22\x22\x22',
        }

    @property
    def default_state(self) -> str:
        return '1'
