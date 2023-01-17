from application.model.routine.move_compost.move_compost_routine import MoveCompostRoutine


class MoveCompostFromBioreactor1ToSieveRoutine(MoveCompostRoutine):
    name = "MoveCompostFromBioreactor1ToSieveRoutine"

    def __init__(self):

        super().__init__('bioreactor1', 'sieve')
