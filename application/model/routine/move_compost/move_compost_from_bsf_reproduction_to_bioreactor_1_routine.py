from application.model.routine.move_compost.move_compost_routine import MoveCompostRoutine


class MoveCompostFromBSFReproductionToBioreactor1Routine(MoveCompostRoutine):
    name = "MoveCompostFromBSFReproductionToBioreactor1Routine"

    def __init__(self):

        super().__init__('bsf_reproduction', 'bioreactor1')
