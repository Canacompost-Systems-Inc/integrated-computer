from application.model.routine.move_compost.move_compost_routine import MoveCompostRoutine


class MoveCompostFromShredderStorageToBioreactor2Routine(MoveCompostRoutine):
    name = "MoveCompostFromShredderStorageToBioreactor2Routine"

    def __init__(self):

        super().__init__('shredder_storage', 'bioreactor2')
