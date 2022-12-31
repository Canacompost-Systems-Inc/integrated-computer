from typing import List

from application.model.sensor.base_sensor import BaseSensor


class SHT40Sensor(BaseSensor):
    """
    Name: SHT40
    DeviceId: 0xC0
    Measurements: Temperature (C), Humidity (%)
    """

    @property
    def device_type_name(self) -> str:
        return 'SHT40'

    @property
    def payload_length(self) -> int:
        return 2

    @property
    def measurement_order(self) -> List[str]:
        return ['temperature', 'humidity']
