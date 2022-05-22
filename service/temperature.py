from mcu.temperature_effector import *

class TemperatureService:

    def __init__(self, temperature_effector):
        self.temperature_effector = temperature_effector

    def setTemperature(self, value):
        return self.temperature_effector.setTemperatureMCU(value)

    def getTemperature(self):
        return self.temperature_effector.getTemperatureMCU()