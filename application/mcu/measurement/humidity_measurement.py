from application.mcu.measurement.base_measurement import BaseMeasurement


class HumidityMeasurement(BaseMeasurement):

    def __init__(self, val):
        self.val = val

    @property
    def name(self) -> str:
        return "humidity"

    @property
    def unit(self) -> str:
        return "%"

    @property
    def normal_max(self) -> float:
        return 80.0

    @property
    def normal_min(self) -> float:
        return 30.0
