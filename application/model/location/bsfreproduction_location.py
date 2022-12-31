from typing import Literal

from application.model.location.base_location import BaseLocation


class BSFReproductionLocation(BaseLocation):
    name = "BSFReproduction"

    @property
    def category(self) -> Literal['input', 'output', 'bioreactor', 'reproduction', 'shared']:
        return 'reproduction'
