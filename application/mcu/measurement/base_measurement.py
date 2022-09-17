from abc import ABC, abstractmethod


class BaseMeasurement(ABC):

    def __str__(self):
        return f"{self.val:.2f} {self.unit} {self.name}"

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
