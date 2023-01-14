from application.model.measurement.base_measurement import BaseMeasurement


class CO2Measurement(BaseMeasurement):

    @property
    def name(self) -> str:
        return "co2"

    @property
    def unit(self) -> str:
        return "ppm"

    @property
    def normal_max(self) -> float:
        return 5000.0

    @property
    def normal_min(self) -> float:
        return 400.0

    @property
    def ideal_max(self) -> float:
        return 1000.0

    @property
    def ideal_min(self) -> float:
        return 0.0
