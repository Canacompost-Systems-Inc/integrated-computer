from application.model.measurement.base_measurement import BaseMeasurement


class TemperatureMeasurement(BaseMeasurement):

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
        return 0.0
