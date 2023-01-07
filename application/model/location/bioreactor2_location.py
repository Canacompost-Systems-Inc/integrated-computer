from typing import Literal

from application.model.location.base_location import BaseLocation


class Bioreactor2Location(BaseLocation):
    name = "Bioreactor2"

    @property
    def category(self) -> Literal['input', 'output', 'bioreactor', 'reproduction', 'shared']:
        return 'bioreactor'
