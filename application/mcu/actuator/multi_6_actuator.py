from abc import ABCMeta
from typing import Dict

from application.mcu.actuator.base_actuator import BaseActuator


class Multi6Actuator(BaseActuator, metaclass=ABCMeta):

    @property
    def possible_states(self) -> Dict[str, bytes]:
        return {
            '1': b'\x11\x11\x11\x11',
            '2': b'\x22\x22\x22\x22',
            '3': b'\x33\x33\x33\x33',
            '4': b'\x44\x44\x44\x44',
            '5': b'\x55\x55\x55\x55',
            '6': b'\x66\x66\x66\x66',
        }

    @property
    def default_state(self) -> str:
        return '1'
