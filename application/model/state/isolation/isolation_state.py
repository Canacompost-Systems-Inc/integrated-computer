from abc import abstractmethod
from typing import Dict

from application.model.location.base_location import BaseLocation
from application.model.state.base_state import BaseState


class IsolationState(BaseState):
    name = "IsolationState"

    @property
    @abstractmethod
    def location_sensor_remapping(self) -> Dict[type(BaseLocation), type(BaseLocation)]:
        """
        Property for remapping the sensor location when this state is active. Used to record the readings for the
        sensors in the AirLoop under a particular Bioreactor or other container.
        """
        pass

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
        from application.model.routine.sanitize_air_loop_routine import SanitizeAirLoopRoutine
        return SanitizeAirLoopRoutine()
