from application.model.measurement.base_measurement import BaseMeasurement


class HumidityMeasurement(BaseMeasurement):

    @property
    def name(self) -> str:
        return "humidity"

    @property
    def unit(self) -> str:
        return "%"

    @property
    def normal_max(self) -> float:
        return 100.0

    @property
    def normal_min(self) -> float:
        return 0.0
