from typing import List

from application.model.sensor.base_sensor import BaseSensor


class IPC10100Sensor(BaseSensor):
    """
    Name: IPC10100
    DeviceId: 0xC2
    Measurements: Temperature (C), Pressure (Pa)
    """

    @property
    def device_type_name(self) -> str:
        return 'IPC10100'

    @property
    def payload_length(self) -> int:
        return 2

    @property
    def measurement_order(self) -> List[str]:
        return ['temperature', 'pressure']
