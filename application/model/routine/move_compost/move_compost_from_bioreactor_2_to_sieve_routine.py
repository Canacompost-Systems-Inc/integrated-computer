from application.model.routine.move_compost.move_compost_routine import MoveCompostRoutine


class MoveCompostFromBioreactor2ToSieveRoutine(MoveCompostRoutine):
    name = "MoveCompostFromBioreactor2ToSieveRoutine"

    def __init__(self):

        super().__init__('bioreactor2', 'sieve')
