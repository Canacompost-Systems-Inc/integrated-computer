from application.model.routine.move_compost.move_compost_routine import MoveCompostRoutine


class MoveCompostFromBSFReproductionToBioreactor2Routine(MoveCompostRoutine):
    name = "MoveCompostFromBSFReproductionToBioreactor2Routine"

    def __init__(self):

        super().__init__('bsf_reproduction', 'bioreactor2')
