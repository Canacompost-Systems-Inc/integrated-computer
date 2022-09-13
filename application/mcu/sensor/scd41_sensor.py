from typing import List

from application.mcu.sensor.base_sensor import BaseSensor


class SCD41Sensor(BaseSensor):
    """
    Name: SCD41
    DeviceId: 0xC1
    Measurements: CO2 (ppm), Temperature (C), Humidity (%)
    """

    @property
    def sensor_name(self) -> str:
        return 'SCD41'

    @property
    def device_id(self) -> str:
        return 'c1'

    @property
    def payload_length(self) -> int:
        return 3

    @property
    def measurement_order(self) -> List[str]:
        return ['co2', 'temperature', 'humidity']
