from application.mcu.measurement.base_measurement import BaseMeasurement


class H2Measurement(BaseMeasurement):

    @property
    def name(self) -> str:
        return "h2"

    @property
    def unit(self) -> str:
        return "ppm"

    @property
    def normal_max(self) -> float:
        return 40.0

    @property
    def normal_min(self) -> float:
        return 2.0
