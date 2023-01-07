from abc import ABCMeta, abstractmethod


class BaseState(metaclass=ABCMeta):
    name = "BaseState"

    def __init__(self, context):
        self.context = context

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return getattr(self, 'name', None) == getattr(other, 'name', None)

    @abstractmethod
    def activate_state(self):
        pass

    @abstractmethod
    def deactivate_state(self):
        pass
