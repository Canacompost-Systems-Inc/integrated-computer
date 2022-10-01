from typing import Dict

from application.mcu.actuator.trinary_actuator import TrinaryActuator


class FlapDiverterValveActuator(TrinaryActuator):

    @property
    def possible_states(self) -> Dict[str, bytes]:
        states = TrinaryActuator().possible_states
        return {
            'starboard': states['0'],
            'middle': states['1'],
            'port': states['2'],
        }

    @property
    def default_state(self) -> str:
        return 'middle'

    @property
    def device_type_name(self) -> str:
        return 'FlapDiverterValve'
