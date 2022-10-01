from abc import ABCMeta
from typing import Dict

from application.mcu.actuator.base_actuator import BaseActuator


class DiscreteStepDegree10Actuator(BaseActuator, metaclass=ABCMeta):

    @property
    def possible_states(self) -> Dict[str, bytes]:
        return {
            '0deg': b'\x00\x00\x00\x00',
            '10deg': b'\x11\x11\x11\x11',
            '20deg': b'\x22\x22\x22\x22',
            '30deg': b'\x33\x33\x33\x33',
            '40deg': b'\x44\x44\x44\x44',
            '50deg': b'\x55\x55\x55\x55',
            '60deg': b'\x66\x66\x66\x66',
            '70deg': b'\x77\x77\x77\x77',
            '80deg': b'\x88\x88\x88\x88',
            '90deg': b'\x99\x99\x99\x99',
        }

    @property
    def default_state(self) -> str:
        return '0deg'
