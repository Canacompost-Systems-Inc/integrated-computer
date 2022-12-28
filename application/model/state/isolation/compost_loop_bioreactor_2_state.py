from application.model.action.activate_air_loop_action_set import ActivateAirLoopActionSet
from application.model.action.activate_compost_loop_source_action_set import ActivateCompostLoopSourceActionSet
from application.model.routine.flush_compost_loop_routine import FlushCompostLoopRoutine
from application.model.routine.routine import Routine
from application.model.routine.routine_step import RoutineStep
from application.model.routine.sanitize_compost_loop_routine import SanitizeCompostLoopRoutine
from application.model.state.isolation.isolation_state import IsolationState


class CompostLoopBioreactor2State(IsolationState):

    def activate_state(self):
        return Routine(steps=[
            RoutineStep(ActivateAirLoopActionSet('compost_loop'), duration_sec=0),
            RoutineStep(ActivateCompostLoopSourceActionSet('bioreactor2'), duration_sec=0),
        ])

    def deactivate_state(self):
        return Routine(steps=[
            RoutineStep(ActivateCompostLoopSourceActionSet(deactivate=True), duration_sec=0),
        ]) + FlushCompostLoopRoutine() + SanitizeCompostLoopRoutine() + FlushCompostLoopRoutine()
