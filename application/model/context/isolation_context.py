from application.model.context.context import Context
from application.model.state.isolation.default_state import DefaultState
from application.model.state.isolation.isolation_state import IsolationState


class IsolationContext(Context):
    """Class for holding the states that deal with system isolation, including which container is active in the air
    loop and compost loop. The IsolationStates implement the requirements for flushing and sanitizing the system when
    switching between states."""

    def __init__(self, default_state: IsolationState = None):
        super().__init__(default_state)
        # Setting this twice so the python type hints work
        self.state = default_state

    def get_state(self) -> IsolationState:
        return self.state

    def change_state(self, new_state: IsolationState):
        yield self.deactivate_state()
        super().change_state(DefaultState(None))  # TODO - figure out if there's a better way to do this - the flush and sanitize require this state
        # yield self.flush_air_loop()
        # yield self.sanitize_air_loop()
        # yield self.flush_air_loop()
        yield self.activate_state()
        super().change_state(new_state)

    # Methods implemented by the individual states
    def activate_state(self):
        return self.state.activate_state()

    def deactivate_state(self):
        return self.state.deactivate_state()

    def flush_air_loop(self):
        return self.state.flush_air_loop()

    def sanitize_air_loop(self):
        return self.state.sanitize_air_loop()
