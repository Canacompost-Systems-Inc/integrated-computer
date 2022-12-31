from typing import List

from application.model.sensor.base_sensor import BaseSensor


class SEN0441Sensor(BaseSensor):
    """
    Name: SEN0441
    Measurements: H2 (ppm)
    """

    @property
    def device_type_name(self) -> str:
        return 'SEN0441'

    @property
    def payload_length(self) -> int:
        return 1

    @property
    def measurement_order(self) -> List[str]:
        return ['h2']
