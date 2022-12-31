from typing import Literal

from application.model.location.base_location import BaseLocation


class AirLoopLocation(BaseLocation):
    name = "AirLoop"

    @property
    def category(self) -> Literal['input', 'output', 'bioreactor', 'reproduction', 'shared']:
        return 'shared'
