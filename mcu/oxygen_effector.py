class OxygenEffector:

    # TODO: Remove this. We will set oxygen via valve control.
    def setOxygenMCU(self, value):
        return "Setting the oxygen to " + value
    
    def getOxygenMCU(self):
        return "Getting oxygen..."