class RoutineRegistryService:
    """
    Routines are sets of actions with timing and dependencies. This class registers the available routines, but does
    not perform them.
    """

    def __init__(self, routine_list):

        self.routine_map = {
            routine.name: routine
            for routine
            in routine_list
        }
