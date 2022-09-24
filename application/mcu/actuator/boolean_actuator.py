from abc import ABCMeta
from typing import Dict

from application.mcu.actuator.base_actuator import BaseActuator


class BooleanActuator(BaseActuator, metaclass=ABCMeta):

    @property
    def possible_states(self) -> Dict[str, bytes]:
        return {
            'low': b'\x00\x00\x00\x00',
            'high': b'\x11\x11\x11\x11',
        }

    @property
    def default_state(self) -> str:
        return 'low'
