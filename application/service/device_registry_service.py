import logging

from application.model.base_device import BaseDevice
from application.service.device_factory import DeviceFactory
from application.service.location_registry_service import LocationRegistryService


class DeviceRegistryService:

    def __init__(self,
                 device_factory: DeviceFactory,
                 location_registry_service: LocationRegistryService,
                 device_map_config: dict,
                 location_aware_sensors: list):

        self.device_factory = device_factory
        self.location_registry_service = location_registry_service
        self.device_map_config = device_map_config
        self.location_aware_sensors = location_aware_sensors

        # Construct an object for each device in the config
        self.device_registry = {}

        for location_name in self.device_map_config:

            location = self.location_registry_service.get_location(location_name)

            for device_id in self.device_map_config[location_name]:
                device_type_name, device_friendly_name = self.device_map_config[location_name][device_id]

                device_is_location_aware = device_id in self.location_aware_sensors

                device_instance = self.device_factory.get_device(
                    device_type_name, device_id, device_friendly_name, location, device_is_location_aware)

                self.device_registry[device_id] = device_instance

    def get_device(self, device_id) -> BaseDevice:
        if device_id not in self.device_registry:
            err = f"Device id '{device_id}' is not registered"
            logging.error(err)
            raise ValueError(err)
        return self.device_registry.get(device_id, None)

    def get_payload_length(self, device_id) -> int:
        """Helper function to get the number of floats in the payload for this device; used when talking to MCU"""
        return self.get_device(device_id).payload_length

    def get_payload_bytes(self, device_id, value) -> bytes:
        """Helper function to get the bytes value of a particular state for an actuator; used when talking to MCU"""
        device = self.get_device(device_id)

        if not self.is_actuator(device_id):
            err = (f"Cannot get payload bytes for possible state '{value}' for device {device.device_type_name} with "
                   f"device_id {device_id} because it is not an actuator")
            logging.error(err)
            raise RuntimeError(err)

        possible_states = device.possible_states

        if value not in possible_states:
            err = f"Unknown value '{value}' for device {device.device_type_name} with device_id {device_id}"
            logging.error(err)
            raise ValueError(err)

        return possible_states.get(value)

    def is_actuator(self, device_id: str) -> bool:
        """Helper function for determining whether this device is an actuator"""
        device = self.get_device(device_id)
        return device.device_category == 'actuator'
