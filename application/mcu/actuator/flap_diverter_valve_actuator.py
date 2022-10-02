from typing import Dict

from application.mcu.actuator.base_actuator import BaseActuator


class FlapDiverterValveActuator(BaseActuator):

    @property
    def possible_states(self) -> Dict[str, bytes]:
        return {
            'left': b'\x00\x00\x00\x00',
            'middle': b'\x00\x00\x00\x01',
            'right': b'\x00\x00\x00\x02',
        }

    @property
    def default_state(self) -> str:
        return 'middle'

    @property
    def device_type_name(self) -> str:
        return 'FlapDiverterValve'
