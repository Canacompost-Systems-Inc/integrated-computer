from typing import Literal

from application.model.location.base_location import BaseLocation


class ShredderStorageLocation(BaseLocation):
    name = "ShredderStorage"

    @property
    def category(self) -> Literal['input', 'output', 'bioreactor', 'reproduction', 'shared']:
        return 'input'
