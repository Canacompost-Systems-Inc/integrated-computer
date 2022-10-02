from typing import Dict

from application.mcu.actuator.base_actuator import BaseActuator


class DiscreteFlapDiverterValveActuator(BaseActuator):

    @property
    def possible_states(self) -> Dict[str, bytes]:
        return {
            '0per': b'\x00\x00\x00\x00',
            '5per': b'\x00\x00\x00\x01',
            '10per': b'\x00\x00\x00\x02',
            '15per': b'\x00\x00\x00\x03',
            '20per': b'\x00\x00\x00\x04',
            '25per': b'\x00\x00\x00\x05',
            '30per': b'\x00\x00\x00\x06',
            '35per': b'\x00\x00\x00\x07',
            '40per': b'\x00\x00\x00\x08',
            '45per': b'\x00\x00\x00\x09',
            '50per': b'\x00\x00\x00\x0a',
            '55per': b'\x00\x00\x00\x0b',
            '60per': b'\x00\x00\x00\x0c',
            '65per': b'\x00\x00\x00\x0d',
            '70per': b'\x00\x00\x00\x0e',
            '75per': b'\x00\x00\x00\x0f',
            '80per': b'\x00\x00\x00\x10',
            '85per': b'\x00\x00\x00\x11',
            '90per': b'\x00\x00\x00\x12',
            '95per': b'\x00\x00\x00\x13',
            '100per': b'\x00\x00\x00\x14',
        }

    @property
    def default_state(self) -> str:
        return '0per'

    @property
    def device_type_name(self) -> str:
        return 'DiscreteFlapDiverterValve'
