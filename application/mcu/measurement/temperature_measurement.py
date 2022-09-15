from application.mcu.measurement.base_measurement import BaseMeasurement


class TemperatureMeasurement(BaseMeasurement):

    def __init__(self, val):
        self.val = val

    @property
    def name(self) -> str:
        return "temperature"

    @property
    def unit(self) -> str:
        return "C"

    @property
    def normal_max(self) -> float:
        return 65.0

    @property
    def normal_min(self) -> float:
        return 15.0
