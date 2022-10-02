from typing import Dict

from application.mcu.actuator.base_actuator import BaseActuator


class ButterflyValveActuator(BaseActuator):

    @property
    def possible_states(self) -> Dict[str, bytes]:
        return {
            '0deg': b'\x00\x00\x00\x00',
            '10deg': b'\x00\x00\x00\x01',
            '20deg': b'\x00\x00\x00\x02',
            '30deg': b'\x00\x00\x00\x03',
            '40deg': b'\x00\x00\x00\x04',
            '50deg': b'\x00\x00\x00\x05',
            '60deg': b'\x00\x00\x00\x06',
            '70deg': b'\x00\x00\x00\x07',
            '80deg': b'\x00\x00\x00\x08',
            '90deg': b'\x00\x00\x00\x09',
        }

    @property
    def default_state(self) -> str:
        return '0deg'

    @property
    def device_type_name(self) -> str:
        return 'ButterflyValve'
