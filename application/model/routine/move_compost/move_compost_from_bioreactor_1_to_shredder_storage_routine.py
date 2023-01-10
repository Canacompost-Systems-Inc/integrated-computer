from application.model.routine.move_compost.move_compost_routine import MoveCompostRoutine


class MoveCompostFromBioreactor1ToShredderStorageRoutine(MoveCompostRoutine):
    name = "MoveCompostFromBioreactor1ToShredderStorageRoutine"

    def __init__(self):

        super().__init__('bioreactor1', 'shredder_storage')
