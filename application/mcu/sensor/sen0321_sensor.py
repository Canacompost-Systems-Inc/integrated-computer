from typing import List

from application.mcu.sensor.base_sensor import BaseSensor


class SEN0321Sensor(BaseSensor):
    """
    Name: SEN0321
    Measurements: O3 (ppm)
    """

    @property
    def device_type_name(self) -> str:
        return 'SEN0321'

    @property
    def payload_length(self) -> int:
        return 1

    @property
    def measurement_order(self) -> List[str]:
        return ['o3']
