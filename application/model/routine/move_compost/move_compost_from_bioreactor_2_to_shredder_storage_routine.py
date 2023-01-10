from application.model.routine.move_compost.move_compost_routine import MoveCompostRoutine


class MoveCompostFromBioreactor2ToShredderStorageRoutine(MoveCompostRoutine):
    name = "MoveCompostFromBioreactor2ToShredderStorageRoutine"

    def __init__(self):

        super().__init__('bioreactor2', 'shredder_storage')
