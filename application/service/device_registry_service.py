import logging

from application.model.base_device import BaseDevice


class DeviceRegistryService:

    def __init__(self, device_factory, device_map_config):

        self.device_factory = device_factory
        self.device_map_config = device_map_config
        self.device_registry = {}

        self.populate_device_registry()

    def populate_device_registry(self):
        """Construct an object for each device in the config"""

        for location in self.device_map_config:
            for device_id in self.device_map_config[location]:
                device_type_name, device_friendly_name = self.device_map_config[location][device_id]

                device_instance = self.device_factory.get_device(
                    device_type_name, device_id, device_friendly_name, location)

                self.device_registry[device_id] = device_instance

    def get_device(self, device_id) -> BaseDevice:
        if device_id not in self.device_registry:
            err = f"Device id '{device_id}' is not registered"
            logging.error(err)
            raise ValueError(err)
        return self.device_registry.get(device_id, None)

    def get_payload_length(self, device_id) -> int:
        return self.get_device(device_id).payload_length

    def get_payload_bytes(self, device_id, value) -> bytes:
        device = self.get_device(device_id)

        if device.device_category != 'actuator':
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
