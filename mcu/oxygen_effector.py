class OxygenEffector:

    def __init__(self):
        self.value = 17 

    # Used as a developer tool, in the real system oxygen should be controlled with valves
    def setOxygenMCU(self, value):
        self.value = value
        print("Setting the oxygen to " + str(value))
    
    def getOxygenMCU(self):
        return self.value