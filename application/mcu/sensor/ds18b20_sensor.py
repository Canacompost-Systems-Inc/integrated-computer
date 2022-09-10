from typing import List

from application.mcu.measurement.base_measurement import BaseMeasurement
from application.mcu.measurement.temperature_measurement import TemperatureMeasurement
from application.mcu.sensor.base_sensor import BaseSensor


class DS18B20Sensor(BaseSensor):

    def device_id(self) -> bytes:
        return 'c3'

    def payload_length(self) -> int:
        return 3

    def read_values(self, payload: str) -> List[BaseMeasurement]:
        val0, _, _ = self.decode_payload(payload)
        return [TemperatureMeasurement(val0)]
