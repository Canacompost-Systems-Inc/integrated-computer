from abc import ABCMeta, abstractmethod


class BaseState(metaclass=ABCMeta):

    def __init__(self, context):
        self.context = context

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return self.__str__()

    @property
    def name(self) -> str:
        return self.__class__.__name__

    @abstractmethod
    def activate_state(self):
        pass

    @abstractmethod
    def deactivate_state(self):
        pass
