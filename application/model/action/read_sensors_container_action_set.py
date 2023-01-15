from typing import Literal

from application.model.action.action import Action
from application.model.action.action_set import ActionSet


class ReadSensorsContainerActionSet(ActionSet):

    def __init__(self,
                 location: Literal['shredder_storage', 'bioreactor1', 'bioreactor2', 'bsf_reproduction'],
                 ):

        # These can be comma separated lists of device ids if more than one sensor exists in the container
        location_mapping = {
            'shredder_storage': 'c3,cd',
            'bioreactor1': 'c4,cb',
            'bioreactor2': 'c5,cc',
            'bsf_reproduction': 'c6,ce',
        }
        values = location_mapping.get(location).split(',')

        super().__init__(iterable=[
            Action(value, None)
            for value in values
        ])
