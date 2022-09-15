from application.mcu.humidity_effector import *

class HumidityService:

    def __init__(self, humidity_effector):
        self.humidity_effector = humidity_effector

    def setHumidity(self, value):
        return self.humidity_effector.setHumidityMCU(value)

    def getHumidity(self):
        return self.humidity_effector.getHumidityMCU()