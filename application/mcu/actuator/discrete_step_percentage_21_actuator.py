from abc import ABCMeta
from typing import Dict

from application.mcu.actuator.base_actuator import BaseActuator


class DiscreteStepPercentage21Actuator(BaseActuator, metaclass=ABCMeta):

    @property
    def possible_states(self) -> Dict[str, bytes]:
        return {
            '0per': b'\x00\x00\x00\x00',
            '5per': b'\x00\x00\x00\x05',
            '10per': b'\x00\x00\x00\x0a',
            '15per': b'\x00\x00\x00\x0f',
            '20per': b'\x00\x00\x00\x14',
            '25per': b'\x00\x00\x00\x19',
            '30per': b'\x00\x00\x00\x1e',
            '35per': b'\x00\x00\x00\x23',
            '40per': b'\x00\x00\x00\x28',
            '45per': b'\x00\x00\x00\x2d',
            '50per': b'\x00\x00\x00\x32',
            '55per': b'\x00\x00\x00\x37',
            '60per': b'\x00\x00\x00\x3c',
            '65per': b'\x00\x00\x00\x41',
            '70per': b'\x00\x00\x00\x46',
            '75per': b'\x00\x00\x00\x4b',
            '80per': b'\x00\x00\x00\x50',
            '85per': b'\x00\x00\x00\x55',
            '90per': b'\x00\x00\x00\x5a',
            '95per': b'\x00\x00\x00\x5f',
            '100per': b'\x00\x00\x00\x64',
        }

    @property
    def default_state(self) -> str:
        return '0per'
