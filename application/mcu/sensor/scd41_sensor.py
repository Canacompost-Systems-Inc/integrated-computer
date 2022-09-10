from typing import List

from application.mcu.measurement.base_measurement import BaseMeasurement
from application.mcu.measurement.co2_measurement import CO2Measurement
from application.mcu.measurement.temperature_measurement import TemperatureMeasurement
from application.mcu.measurement.humidity_measurement import HumidityMeasurement
from application.mcu.sensor.base_sensor import BaseSensor


class SCD41Sensor(BaseSensor):

    def device_id(self) -> bytes:
        return 'c1'

    def payload_length(self) -> int:
        return 3

    def read_values(self, payload: str) -> List[BaseMeasurement]:
        val0, val1, val2 = self.decode_payload(payload)
        return [CO2Measurement(val0), TemperatureMeasurement(val1), HumidityMeasurement(val2)]
