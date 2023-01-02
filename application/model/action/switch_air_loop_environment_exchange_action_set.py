from application.model.action.action import Action
from application.model.action.action_set import ActionSet


class SwitchAirLoopEnvironmentExchangeActionSet(ActionSet):

    def __init__(self,
                 strength='0'
                 ):

        super().__init__(iterable=[
            Action('eb', strength),
            Action('ec', strength)
        ])
