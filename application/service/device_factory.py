from application.model.base_device import BaseDevice


class DeviceFactory:

    def __init__(self, device_types_list):

        self.device_types_map = {
            d().device_type_name: d
            for d
            in device_types_list
        }

    def get_device(self, device_type_name, device_id, device_friendly_name, location, is_location_aware) -> BaseDevice:

        if device_type_name not in self.device_types_map:
            raise ValueError(f"Unknown device type name '{device_type_name}'")

        device_class = self.device_types_map.get(device_type_name)
        device_instance = device_class(device_id, device_friendly_name, location, is_location_aware)

        return device_instance
