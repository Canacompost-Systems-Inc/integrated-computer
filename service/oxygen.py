from mcu.oxygen_effector import *

class OxygenService:

    def __init__(self, oxygen_effector):
        self.oxygen_effector = oxygen_effector

    # TODO: Remove this. Oxygen will be controlled via valve management
    def setOxygen(self, value):
        return self.oxygen_effector.setOxygenMCU(value)

    def getOxygen(self):
        return "Getting the oxygen..."