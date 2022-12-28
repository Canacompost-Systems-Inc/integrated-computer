from abc import abstractmethod

from application.model.state.base_state import BaseState


class IsolationState(BaseState):

    @abstractmethod
    def activate_state(self):
        pass

    @abstractmethod
    def deactivate_state(self):
        pass

    def flush_air_loop(self):
        # Note - we need to import here to avoid circular imports (only happens due to type hints)
        from application.model.routine.flush_air_loop_routine import FlushAirLoopRoutine
        return FlushAirLoopRoutine()

    def sanitize_air_loop(self):
        # Note - we need to import here to avoid circular imports (only happens due to type hints)
        from application.model.routine.flush_air_loop_routine import FlushAirLoopRoutine
        from application.model.routine.sanitize_air_loop_routine import SanitizeAirLoopRoutine
        return SanitizeAirLoopRoutine() + FlushAirLoopRoutine()
