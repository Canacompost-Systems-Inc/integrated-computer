from application.model.measurement.base_measurement import BaseMeasurement


class O3Measurement(BaseMeasurement):

    @property
    def name(self) -> str:
        return "o3"

    @property
    def unit(self) -> str:
        return "ppb"

    @property
    def normal_max(self) -> float:
        return 100.0

    @property
    def normal_min(self) -> float:
        return 0.0
