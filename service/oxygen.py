from mcu.oxygen_effector import *

class OxygenService:

    def __init__(self, oxygen_effector):
        self.oxygen_effector = oxygen_effector

    def setOxygen(self, value):
        return self.oxygen_effector.setOxygenMCU(value)

    def getOxygen(self):
        return self.oxygen_effector.getOxygenMCU()