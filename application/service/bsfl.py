from application.mcu.humidity_effector import *

class BSFLService:

    def __init__(self, bsfl_effector):
        self.bsfl_effector = bsfl_effector

    def setBSFL(self, value):
        return self.bsfl_effector.setBSFLMCU(value)

    def getBSFL(self):
        return self.bsfl_effector.getBSFLMCU()