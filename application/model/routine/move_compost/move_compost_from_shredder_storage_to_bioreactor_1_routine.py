from application.model.routine.move_compost.move_compost_routine import MoveCompostRoutine


class MoveCompostFromShredderStorageToBioreactor1Routine(MoveCompostRoutine):
    name = "MoveCompostFromShredderStorageToBioreactor1Routine"

    def __init__(self):

        super().__init__('shredder_storage', 'bioreactor1')
