from application.mcu.measurement.base_measurement import BaseMeasurement


class StateMeasurement(BaseMeasurement):

    @property
    def name(self) -> str:
        return "state"

    @property
    def unit(self) -> str:
        return ""

    @property
    def normal_max(self) -> float:
        return 0

    @property
    def normal_min(self) -> float:
        return 0
