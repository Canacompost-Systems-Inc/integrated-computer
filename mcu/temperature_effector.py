class TemperatureEffector:

    # TODO: Remove this. We will set temperature via valve control.
    def setTemperatureMCU(self, value):
        return "Setting the temperature to " + value
    
    def getTemperatureMCU(self):
        return "Getting temperature..."