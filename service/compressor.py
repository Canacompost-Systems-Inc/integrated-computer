from datetime import datetime
from service.model.routine import Routine

class CompressorService:

    def __init__(self, compressor_effector):
        self.compressor_effector = compressor_effector
        self.compressor_state = False # TODO: Move this to a DB or poll compressor MCU
        self.last_start = datetime.now()
        self.last_stop = datetime.now()

    def getLastStart(self):
        return self.last_start

    def getLastStop(self):
        return self.last_stop
        
    def setCompressor(self, routine: Routine):
        self.compressor_effector.setCompressor(routine.compressor)
        if routine.compressor and not self.compressor_state:
            self.last_start = datetime.now() # TODO: Remember to handle 2 second delay. If this is asynchronous we might have to add it here.
        if not routine.compressor and self.compressor_state:
            self.last_stop = datetime.now() # TODO: Remember to handle 2 second delay. If this is asynchronous we might have to add it here.
        self.compressor_state = routine.compressor