from abc import ABCMeta, abstractmethod
from typing import Literal


class BaseLocation(metaclass=ABCMeta):
    name = "BaseLocation"

    def __init__(self):
        pass

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return getattr(self, 'name', None) == getattr(other, 'name', None)

    @property
    @abstractmethod
    def category(self) -> Literal['input', 'output', 'bioreactor', 'reproduction', 'shared']:
        pass

    @property
    def is_container(self) -> bool:
        return self.category in ['input', 'output', 'bioreactor', 'reproduction']
