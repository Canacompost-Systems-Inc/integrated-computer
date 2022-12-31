from typing import Dict

from application.model.action.activate_air_loop_action_set import ActivateAirLoopActionSet
from application.model.action.activate_compost_loop_source_action_set import ActivateCompostLoopSourceActionSet
from application.model.location.base_location import BaseLocation
from application.model.location.bioreactor1_location import Bioreactor1Location
from application.model.location.compostloop_location import CompostLoopLocation
from application.model.routine.flush_compost_loop_routine import FlushCompostLoopRoutine
from application.model.routine.routine import Routine
from application.model.routine.routine_step import RoutineStep
from application.model.routine.sanitize_compost_loop_routine import SanitizeCompostLoopRoutine
from application.model.state.isolation.isolation_state import IsolationState


class CompostLoopBioreactor1State(IsolationState):
    name = "CompostLoopBioreactor1State"

    @property
    def location_sensor_remapping(self) -> Dict[type(BaseLocation), type(BaseLocation)]:
        return {
            CompostLoopLocation: Bioreactor1Location,
        }

    def activate_state(self):
        return Routine(steps=[
            RoutineStep(ActivateAirLoopActionSet('compost_loop'), duration_sec=0),
            RoutineStep(ActivateCompostLoopSourceActionSet('bioreactor1'), duration_sec=0),
        ])

    def deactivate_state(self):
        return Routine(steps=[
            RoutineStep(ActivateCompostLoopSourceActionSet(deactivate=True), duration_sec=0),
        ]) + FlushCompostLoopRoutine() + SanitizeCompostLoopRoutine() + FlushCompostLoopRoutine()
