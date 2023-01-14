from typing import List

from application.model.measurement.base_measurement import BaseMeasurement


class MeasurementFactory:

    def __init__(self, measurements_list):

        self.measurement_class_map = {
            measurement_class(0).name: measurement_class
            for measurement_class
            in measurements_list
        }

    def get_measurement(self, measurement_type_name, value) -> BaseMeasurement:

        if measurement_type_name not in self.measurement_class_map:
            raise ValueError(f"Unknown measurement type name '{measurement_type_name}'")

        measurement_class = self.measurement_class_map.get(measurement_type_name)
        measurement_instance = measurement_class(value)

        return measurement_instance

    @property
    def available_measurements(self) -> List[str]:
        return list(self.measurement_class_map.keys())
