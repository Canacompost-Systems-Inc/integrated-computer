from typing import List

from application.mcu.sensor.base_sensor import BaseSensor


class DS18B20Sensor(BaseSensor):
    """
    Name: DS18B20
    DeviceId: 0xC3
    Measurements: Temperature (C)
    """

    @property
    def device_type_name(self) -> str:
        return 'DS18B20'

    @property
    def payload_length(self) -> int:
        return 3

    @property
    def measurement_order(self) -> List[str]:
        return ['temperature']
