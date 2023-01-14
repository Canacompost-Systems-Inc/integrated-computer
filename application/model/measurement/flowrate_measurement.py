from application.model.measurement.base_measurement import BaseMeasurement


class FlowRateMeasurement(BaseMeasurement):

    @property
    def name(self) -> str:
        return "flowrate"

    @property
    def unit(self) -> str:
        return "L/min"

    @property
    def normal_max(self) -> float:
        return 30.0

    @property
    def normal_min(self) -> float:
        return 0.0

    @property
    def ideal_max(self) -> float:
        return 20.0

    @property
    def ideal_min(self) -> float:
        return 0.0
