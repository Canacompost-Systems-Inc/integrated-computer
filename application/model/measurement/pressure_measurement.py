from application.model.measurement.base_measurement import BaseMeasurement


class PressureMeasurement(BaseMeasurement):

    @property
    def name(self) -> str:
        return "pressure"

    @property
    def unit(self) -> str:
        return "Pa"

    @property
    def normal_max(self) -> float:
        return 105000.0

    @property
    def normal_min(self) -> float:
        return 95000.0

    @property
    def ideal_max(self) -> float:
        return 102000.0

    @property
    def ideal_min(self) -> float:
        return 98000.0
