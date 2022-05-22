from service.model.routine import Routine

class WaterPumpService:

    def __init__(self, water_pump_effector):
        self.water_pump_effector = water_pump_effector

    def setWaterPump(self, routine: Routine):
        self.water_pump_effector.setWaterPump(routine.waterPump)