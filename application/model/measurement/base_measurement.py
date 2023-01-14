from abc import ABCMeta, abstractmethod


class BaseMeasurement(metaclass=ABCMeta):

    def __init__(self, val):
        self.val = val

    def __str__(self):
        val = f"{self.val:.2f}" if isinstance(self.val, float) else f"{self.val}"
        return f"{val} {self.unit} {self.name}"

    def __repr__(self):
        return self.__str__()

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def unit(self) -> str:
        pass

    @property
    @abstractmethod
    def normal_max(self) -> float:
        pass

    @property
    @abstractmethod
    def normal_min(self) -> float:
        pass

    @property
    @abstractmethod
    def ideal_max(self) -> float:
        pass

    @property
    @abstractmethod
    def ideal_min(self) -> float:
        pass
