from typing import Literal

from application.model.location.base_location import BaseLocation


class Bioreactor1Location(BaseLocation):
    name = "Bioreactor1"

    @property
    def category(self) -> Literal['input', 'output', 'bioreactor', 'reproduction', 'shared']:
        return 'bioreactor'
