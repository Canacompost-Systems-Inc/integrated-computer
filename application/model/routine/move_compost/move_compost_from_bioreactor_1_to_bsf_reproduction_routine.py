from application.model.routine.move_compost.move_compost_routine import MoveCompostRoutine


class MoveCompostFromBioreactor1ToBSFReproductionRoutine(MoveCompostRoutine):
    name = "MoveCompostFromBioreactor1ToBSFReproductionRoutine"

    def __init__(self):

        super().__init__('bioreactor1', 'bsf_reproduction')
