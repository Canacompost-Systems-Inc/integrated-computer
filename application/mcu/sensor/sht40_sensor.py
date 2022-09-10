from typing import List

from application.mcu.measurement.base_measurement import BaseMeasurement
from application.mcu.measurement.temperature_measurement import TemperatureMeasurement
from application.mcu.measurement.humidity_measurement import HumidityMeasurement
from application.mcu.sensor.base_sensor import BaseSensor


class SHT40Sensor(BaseSensor):

    def device_id(self) -> bytes:
        return 'c0'

    def payload_length(self) -> int:
        return 3

    def read_values(self, payload: str) -> List[BaseMeasurement]:
        val0, val1, _ = self.decode_payload(payload)
        return [TemperatureMeasurement(val0), HumidityMeasurement(val1)]
