class OxygenEffector:

    def __init__(self):
        self.value = 18 # Assume atmospheric norm until we can read from the sensor

    # Used as a developer tool, in the real system oxygen should be controlled with valves
    def setOxygenMCU(self, value):
        self.value = value
        print("Setting the oxygen to " + str(value))
    
    def getOxygenMCU(self):
        return self.value