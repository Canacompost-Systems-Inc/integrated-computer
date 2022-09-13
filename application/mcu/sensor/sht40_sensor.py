from typing import List

from application.mcu.sensor.base_sensor import BaseSensor


class SHT40Sensor(BaseSensor):
    """
    Name: SHT40
    DeviceId: 0xC0
    Measurements: Temperature (C), Humidity (%)
    """

    @property
    def sensor_name(self) -> str:
        return 'SHT40'

    @property
    def device_id(self) -> str:
        return 'c0'

    @property
    def payload_length(self) -> int:
        return 3

    @property
    def measurement_order(self) -> List[str]:
        return ['temperature', 'humidity']
