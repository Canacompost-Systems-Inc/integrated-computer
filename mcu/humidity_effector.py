class HumidityEffector:

    def __init__(self):
        self.value = 79

    # Used as a developer tool, in the real system oxygen should be controlled with valves
    def setHumidityMCU(self, value):
        self.value = value
        print("Setting the humidity to " + str(value))
    
    def getHumidityMCU(self):
        return self.value