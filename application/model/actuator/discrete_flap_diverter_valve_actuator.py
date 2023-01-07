from typing import Dict

from application.model.actuator.base_actuator import BaseActuator


class DiscreteFlapDiverterValveActuator(BaseActuator):

    @property
    def possible_states(self) -> Dict[str, bytes]:
        return {
            '0': b'\x00\x00\x00\x00',
            '5': b'\x00\x00\x00\x01',
            '10': b'\x00\x00\x00\x02',
            '15': b'\x00\x00\x00\x03',
            '20': b'\x00\x00\x00\x04',
            '25': b'\x00\x00\x00\x05',
            '30': b'\x00\x00\x00\x06',
            '35': b'\x00\x00\x00\x07',
            '40': b'\x00\x00\x00\x08',
            '45': b'\x00\x00\x00\x09',
            '50': b'\x00\x00\x00\x0a',
            '55': b'\x00\x00\x00\x0a',
            '60': b'\x00\x00\x00\x0b',
            '65': b'\x00\x00\x00\x0c',
            '70': b'\x00\x00\x00\x0d',
            '75': b'\x00\x00\x00\x0e',
            '80': b'\x00\x00\x00\x0f',
            '85': b'\x00\x00\x00\x10',
            '90': b'\x00\x00\x00\x11',
            '95': b'\x00\x00\x00\x12',
            '100': b'\x00\x00\x00\x13',
        }

    @property
    def default_state(self) -> str:
        return '50'

    @property
    def device_type_name(self) -> str:
        return 'DiscreteFlapDiverterValve'
