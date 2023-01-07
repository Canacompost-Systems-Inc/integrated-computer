from typing import List

from application.model.location.base_location import BaseLocation


class LocationRegistryService:
    """
    Locations are the containers and the shared infrastructure (air loop and compost loop. This class registers the
    instances of each location.
    """

    def __init__(self, location_list: List[type(BaseLocation)]):

        self.location_map = {
            location.name: location()
            for location
            in location_list
        }

    def all_locations(self) -> List[BaseLocation]:
        return list(self.location_map.values())

    def get_location(self, location_name: str) -> BaseLocation:
        if location_name not in self.location_map:
            raise ValueError(f"Location name '{location_name}' is not registered")
        return self.location_map.get(location_name, None)
