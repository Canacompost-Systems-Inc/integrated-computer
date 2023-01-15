from typing import Dict

from application.model.action.set_rotary_valve_compost_loop_action_set import SetRotaryValveCompostLoopActionSet
from application.model.action.set_rotary_valve_from_air_loop_action_set import SetRotaryValveFromAirLoopActionSet
from application.model.action.set_rotary_valve_to_air_loop_action_set import SetRotaryValveToAirLoopActionSet
from application.model.location.base_location import BaseLocation
from application.model.routine.routine import Routine
from application.model.routine.routine_step import RoutineStep
from application.model.state.isolation.isolation_state import IsolationState


class DefaultState(IsolationState):
    name = "DefaultState"

    @property
    def location_sensor_remapping(self) -> Dict[type(BaseLocation), type(BaseLocation)]:
        return {}

    def activate_state(self):
        return Routine(steps=[
            RoutineStep(SetRotaryValveToAirLoopActionSet('compost_loop'), then_wait_n_sec=0),
            RoutineStep(SetRotaryValveCompostLoopActionSet('air_loop'), then_wait_n_sec=0),
            RoutineStep(SetRotaryValveFromAirLoopActionSet('compost_loop'), then_wait_n_sec=0),
        ])

    def deactivate_state(self):
        # Nothing is required to deactivate the default state
        return Routine(steps=[])
