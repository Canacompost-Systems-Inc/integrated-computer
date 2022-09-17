from application.mcu.measurement.base_measurement import BaseMeasurement


class PressureMeasurement(BaseMeasurement):

    def __init__(self, val):
        self.val = val

    @property
    def name(self) -> str:
        return "pressure"

    @property
    def unit(self) -> str:
        return "Pa"

    @property
    def normal_max(self) -> float:
        return 2.0

    @property
    def normal_min(self) -> float:
        return 1.0
