from typing import Literal

from application.model.action.action import Action
from application.model.action.action_set import ActionSet


class SwitchAirHammerActionSet(ActionSet):

    def __init__(self,
                 location: Literal['shredder_storage', 'bioreactor1', 'bioreactor2', 'bsf_reproduction'],
                 to: Literal['open', 'close'] = 'close',
                 ):

        # TODO - commenting out while these are not connected

        location_mapping = {
            'shredder_storage': '',  # ed
            'bioreactor1': '',  # ee
            'bioreactor2': '',  # ef
            'bsf_reproduction': 'f0'  # f0
        }
        value = location_mapping.get(location)

        # TODO - comment this out once all air hammer relays are connected
        if not value:
            super().__init__(iterable=[])
            return

        super().__init__(iterable=[
            Action(value, to)
        ])
