from mcu.valve_effector import *
from service.model.routine import Routine

class ValvesService:

    def __init__(self, valve_effector):
        self.valve_effector = valve_effector

    def setValves(self, routine: Routine):
        self.valve_effector.setValves(routine.v1, routine.v2, routine.v3, routine.v4, routine.v5, routine.v6)