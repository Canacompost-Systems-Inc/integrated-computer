from typing import Literal

from application.model.action.action import Action
from application.model.action.action_set import ActionSet


class SetRotaryValveToAirLoopActionSet(ActionSet):

    def __init__(self,
                 location: Literal['compost_loop', 'shredder_storage', 'bioreactor1', 'bioreactor2',
                                   'bsf_reproduction'] = 'compost_loop',
                 ):

        # Open: 0
        location_mapping = {
            'compost_loop': '1',
            'shredder_storage': '2',
            'bioreactor1': '4',
            'bioreactor2': '5',
            'bsf_reproduction': '3',
        }
        value = location_mapping.get(location)

        super().__init__(iterable=[
            Action('e1', value)
        ])
