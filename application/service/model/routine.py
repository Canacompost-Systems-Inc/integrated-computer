class Routine:

    def __init__(self, routineMap):
        # Null checks & format validation
        self.v1 = routineMap["V1"]
        self.v2 = routineMap["V2"]
        self.v3 = routineMap["V3"]
        self.v4 = routineMap["V4"]
        self.v5 = routineMap["V5"]
        self.v6 = routineMap["V6"]
        self.compressor = routineMap["Compressor"]
        self.waterPump = routineMap["WaterPump"]