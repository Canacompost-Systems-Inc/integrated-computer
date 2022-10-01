from abc import ABCMeta
from typing import Dict

from application.mcu.actuator.base_actuator import BaseActuator


class BinaryOpenCloseActuator(BaseActuator, metaclass=ABCMeta):

    @property
    def possible_states(self) -> Dict[str, bytes]:
        return {
            'close': b'\x00\x00\x00\x00',
            'open': b'\x11\x11\x11\x11',
        }

    @property
    def default_state(self) -> str:
        return 'close'
