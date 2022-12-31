from abc import ABCMeta
from typing import Dict

from application.model.actuator.base_actuator import BaseActuator


class BinaryOnOffActuator(BaseActuator, metaclass=ABCMeta):

    @property
    def possible_states(self) -> Dict[str, bytes]:
        return {
            'off': b'\x00\x00\x00\x00',
            'on': b'\x00\x00\x00\x01',
        }

    @property
    def default_state(self) -> str:
        return 'off'
