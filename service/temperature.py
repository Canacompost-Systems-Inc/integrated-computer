from mcu.temperature_effector import *

class TemperatureService:

    def __init__(self, temperature_effector):
        self.temperature_effector = temperature_effector

    # TODO: Remove this. Temperature will be controlled via valve management
    def setTemperature(self, value):
        return self.temperature_effector.setTemperatureMCU(value)

    def getTemperature(self):
        return "Getting the temperature..."