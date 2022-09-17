class TemperatureEffector:

    def __init__(self):
        self.value = 30 # Assume atmospheric norm until we can read from the sensor

    # Used as a developer tool, in the real system temperature should be controlled with valves
    def setTemperatureMCU(self, value):
        self.value = value
        print("Setting the temperature to " + str(value))
    
    def getTemperatureMCU(self):
        return self.value