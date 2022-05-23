class BSFLEffector:

    def __init__(self):
        self.value = False # Assume system starts with no BSFL
    
    def setBSFLMCU(self, value):
        self.value = value
        print("Setting the BSFL to " + str(value))
    
    def getBSFLMCU(self):
        return self.value