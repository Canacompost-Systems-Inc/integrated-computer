from typing import Literal

from application.model.location.base_location import BaseLocation


class SieveLocation(BaseLocation):
    name = "Sieve"

    @property
    def category(self) -> Literal['input', 'output', 'bioreactor', 'reproduction', 'shared']:
        return 'output'
