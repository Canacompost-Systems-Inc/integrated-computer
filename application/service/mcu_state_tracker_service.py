import logging
from typing import Dict, List, Optional

from application.model.datum import Datum
from application.model.context.isolation_context import IsolationContext
from application.service.device_registry_service import DeviceRegistryService
from application.service.location_registry_service import LocationRegistryService


class MCUStateTrackerService:
    """
    Responsible for tracking the last read state of the system, including sensor readings.

    # TODO - in the future, this service can store these values in the DB for persistence
    """

    def __init__(self, device_registry_service: DeviceRegistryService,
                 location_registry_service: LocationRegistryService,
                 isolation_context: IsolationContext):
        self.device_registry_service = device_registry_service
        self.location_registry_service = location_registry_service
        self.isolation_context = isolation_context

        self.last_read_actuator_states: Dict[str, Datum] = {}
        self.last_read_measurements: Dict[str, Dict[str, Dict[str, Datum]]] = {}

        # Only track measurements for container locations
        for location in self.location_registry_service.all_locations():
            self.last_read_measurements[location.name] = {}

    def update_tracked_state(self, mcu_service_response: Dict[str, List[Datum]]):
        """Take the response from the MCU Service, which is a mapping from device_id > [Datum objects], and update
        the last_read mappings.
        """

        current_isolation_state = self.isolation_context.get_state()
        still_initializing = current_isolation_state is None  # This is set to None during initialization

        # Record the sensor measurements in the right location based on the isolation state
        location_remapping = {}
        if not still_initializing:

            # TODO - clean this up because it's ugly
            for from_location, to_location in current_isolation_state.location_sensor_remapping.items():
                from_name = from_location.name
                to_name = to_location.name
                location_remapping[from_name] = self.location_registry_service.get_location(to_name)

                # logging.debug(
                #     f"Recording measurements from {from_name} as {to_name} because the isolation state "
                #     f"{self.isolation_context.state} is active")

        for device_id, datum_list in mcu_service_response.items():

            is_actuator = self.device_registry_service.is_actuator(device_id)

            if is_actuator:

                state_measurement = datum_list[0]  # Actuators return only one datum, which has a 'state' measurement
                self.last_read_actuator_states[device_id] = state_measurement

            else:

                if still_initializing:
                    continue

                for datum in datum_list:
                    location = datum.device.location
                    measurement_name = datum.measurement.name

                    # Do the remapping only if this device is location aware
                    is_location_aware = datum.device.is_location_aware
                    if is_location_aware:
                        location_name = location_remapping.get(location.name, location).name
                    else:
                        location_name = location.name

                    if location_name not in self.last_read_measurements:
                        continue

                    if measurement_name not in self.last_read_measurements[location_name]:
                        self.last_read_measurements[location_name][measurement_name] = {}

                    self.last_read_measurements[location_name][measurement_name][device_id] = datum

    def get_actuator_states(self) -> Dict[str, str]:
        actuator_states = {}

        for device_id, state_measurement in self.last_read_actuator_states.items():
            actuator_states[device_id] = state_measurement.measurement.val

        return actuator_states

    def get_latest_measurements(self) -> Dict[str, Dict[str, str]]:
        measurement_by_location = {}

        for location in self.last_read_measurements:
            measurement_by_location[location] = {}

            for measurement_name in self.last_read_measurements[location]:

                datum_objects = self.last_read_measurements[location][measurement_name].values()

                # For now, take the average of all readings
                # TODO - in the future, make this smarter
                float_values = [datum.measurement.val for datum in datum_objects]

                # TODO - how to handle units? for now, just returning the value
                # unique_units = list(set(datum.measurement.unit for datum in datum_objects))
                # if len(unique_units) > 1:
                #     raise RuntimeError(f"Cannot average measurements from multiple units: {unique_units}")
                # unit = unique_units[0]

                averaged_value = float(sum(float_values)/len(float_values))

                measurement_by_location[location][measurement_name] = f"{averaged_value:.2f}"

        return measurement_by_location
