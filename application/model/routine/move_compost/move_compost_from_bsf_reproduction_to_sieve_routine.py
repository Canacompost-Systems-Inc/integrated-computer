from application.model.routine.move_compost.move_compost_routine import MoveCompostRoutine


class MoveCompostFromBSFReproductionToSieveRoutine(MoveCompostRoutine):
    name = "MoveCompostFromBSFReproductionToSieveRoutine"

    def __init__(self):

        super().__init__('bsf_reproduction', 'sieve')
