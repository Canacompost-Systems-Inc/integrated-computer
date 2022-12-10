from typing import Dict

from application.mcu.actuator.base_actuator import BaseActuator


class FlapDiverterValveActuator(BaseActuator):

    @property
    def possible_states(self) -> Dict[str, bytes]:
        return {
            'through': b'\x00\x00\x00\x00',
            'divert': b'\x00\x00\x00\x01',
        }

    @property
    def default_state(self) -> str:
        return 'through'

    @property
    def device_type_name(self) -> str:
        return 'FlapDiverterValve'
