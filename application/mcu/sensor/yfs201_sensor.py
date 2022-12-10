from typing import List

from application.mcu.sensor.base_sensor import BaseSensor


class YFS201Sensor(BaseSensor):
    """
    Name: YFS201
    Measurements: FlowRate (L/min)
    """

    @property
    def device_type_name(self) -> str:
        return 'YFS201'

    @property
    def payload_length(self) -> int:
        return 1

    @property
    def measurement_order(self) -> List[str]:
        return ['flowrate']
