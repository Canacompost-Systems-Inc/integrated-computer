from typing import List

from application.mcu.measurement.base_measurement import BaseMeasurement
from application.mcu.measurement.temperature_measurement import TemperatureMeasurement
from application.mcu.measurement.pressure_measurement import PressureMeasurement
from application.mcu.sensor.base_sensor import BaseSensor


class IPC10100Sensor(BaseSensor):

    def device_id(self) -> bytes:
        return 'c2'

    def payload_length(self) -> int:
        return 3

    def read_values(self, payload: str) -> List[BaseMeasurement]:
        val0, val1, _ = self.decode_payload(payload)
        return [TemperatureMeasurement(val0), PressureMeasurement(val1)]
