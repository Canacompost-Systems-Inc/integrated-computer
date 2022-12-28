from abc import ABCMeta

from application.model.state.base_state import BaseState


class Context(metaclass=ABCMeta):
    """Context object for the state design pattern."""

    def __init__(self, default_state: BaseState):
        self.state = default_state

    def __str__(self):
        return f"{self.__class__.__name__} with current state {self.state}"

    def __repr__(self):
        return self.__str__()

    def change_state(self, new_state: BaseState):
        self.state = new_state
