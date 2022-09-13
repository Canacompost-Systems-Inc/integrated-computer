from application.mcu.measurement.base_measurement import BaseMeasurement


class CO2Measurement(BaseMeasurement):

    def __init__(self, val):
        self.val = val

    @property
    def name(self) -> str:
        return "co2"

    @property
    def unit(self) -> str:
        return "%"

    @property
    def normal_max(self) -> float:
        return 40.0

    @property
    def normal_min(self) -> float:
        return 2.0