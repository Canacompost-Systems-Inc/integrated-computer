from typing import Dict

from application.model.action.activate_air_loop_action_set import ActivateAirLoopActionSet
from application.model.action.activate_compost_loop_source_action_set import ActivateCompostLoopSourceActionSet
from application.model.location.base_location import BaseLocation
from application.model.location.bioreactor2_location import Bioreactor2Location
from application.model.location.compostloop_location import CompostLoopLocation
from application.model.routine.flush_compost_loop_routine import FlushCompostLoopRoutine
from application.model.routine.routine import Routine
from application.model.routine.routine_step import RoutineStep
from application.model.routine.sanitize_compost_loop_routine import SanitizeCompostLoopRoutine
from application.model.state.isolation.isolation_state import IsolationState


class CompostLoopBioreactor2State(IsolationState):
    name = "CompostLoopBioreactor2State"

    @property
    def location_sensor_remapping(self) -> Dict[type(BaseLocation), type(BaseLocation)]:
        return {
            CompostLoopLocation: Bioreactor2Location,
        }

    def activate_state(self):
        return Routine(steps=[
            RoutineStep(ActivateAirLoopActionSet('compost_loop'), then_wait_n_sec=0),
            RoutineStep(ActivateCompostLoopSourceActionSet('bioreactor2'), then_wait_n_sec=0),
        ])

    def deactivate_state(self):
        return Routine(steps=[
            RoutineStep(ActivateCompostLoopSourceActionSet(deactivate=True), then_wait_n_sec=0),
        ]) + FlushCompostLoopRoutine() + SanitizeCompostLoopRoutine()
