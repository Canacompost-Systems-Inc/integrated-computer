from service.model.routine import Routine

class CompressorService:

    def __init__(self, compressor_effector):
        self.compressor_effector = compressor_effector

    def setCompressor(self, routine: Routine):
        self.compressor_effector.setCompressor(routine.compressor)