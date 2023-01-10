from application.model.routine.move_compost.move_compost_routine import MoveCompostRoutine


class MoveCompostFromBioreactor2ToBSFReproductionRoutine(MoveCompostRoutine):
    name = "MoveCompostFromBioreactor2ToBSFReproductionRoutine"

    def __init__(self):

        super().__init__('bioreactor2', 'bsf_reproduction')
