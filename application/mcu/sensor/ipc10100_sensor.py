from typing import List

from application.mcu.sensor.base_sensor import BaseSensor


class IPC10100Sensor(BaseSensor):
    """
    Name: IPC10100
    DeviceId: 0xC2
    Measurements: Temperature (C), Pressure (Pa)
    """

    @property
    def sensor_name(self) -> str:
        return 'IPC10100'

    @property
    def device_id(self) -> str:
        return 'c2'

    @property
    def payload_length(self) -> int:
        return 3

    @property
    def measurement_order(self) -> List[str]:
        return ['temperature', 'pressure']
