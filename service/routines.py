from service.model.routine import *

class RoutinesService():
    """
    The RoutineService executes routines on the recycler
    """

    # Machine state for each routine
    # TODO: Move this to a config file
    routineMap = {
        "R0": { # Default routine. The "do nothing" state.
            "V1": False,
            "V2": False,
            "V3": False,
            "V4": False,
            "V5": False,
            "V6": False,
            "Compressor": False,
            "WaterPump": False
        },
        "R1": { # Lower temperature
            "V1": True,
            "V2": False,
            "V3": True,
            "V4": False,
            "V5": False,
            "V6": True,
            "Compressor": True,
            "WaterPump": False
        },
        "R2": { # Lower humidity
            "V1": True,
            "V2": False,
            "V3": True,
            "V4": False,
            "V5": False,
            "V6": True,
            "Compressor": True,
            "WaterPump": False
        },
        "R3": { # Raise humidity
            "V1": False,
            "V2": False,
            "V3": False,
            "V4": False,
            "V5": False,
            "V6": False,
            "Compressor": False,
            "WaterPump": True
        },
        "R4": { # Raise Oxygen
            "V1": True,
            "V2": True,
            "V3": False,
            "V4": True,
            "V5": True,
            "V6": False,
            "Compressor": False,
            "WaterPump": False
        },
        "R5": { # Air Cycle
            "V1": True,
            "V2": False,
            "V3": True,
            "V4": False,
            "V5": True,
            "V6": False,
            "Compressor": True,
            "WaterPump": False
        }
    }

    def __init__(self, valves, compressor, water_pump):
        self.r0 = Routine(self.routineMap["R0"])
        self.r1 = Routine(self.routineMap["R1"])
        self.r2 = Routine(self.routineMap["R2"])
        self.r3 = Routine(self.routineMap["R3"])
        self.r4 = Routine(self.routineMap["R4"])
        self.r5 = Routine(self.routineMap["R5"])
        self.valves = valves
        self.compressor = compressor
        self.water_pump = water_pump

    def startR0(self):
        print("Starting routine: 0, Default")
        self.valves.setValves(self.r0)
        self.compressor.setCompressor(self.r0)
        self.water_pump.setWaterPump(self.r0)

    def startR1(self):
        print("Starting routine: 1, Lower Temp")
        self.valves.setValves(self.r1)
        self.compressor.setCompressor(self.r1)
        self.water_pump.setWaterPump(self.r1)

    def startR2(self):
        print("Starting routine: 2, Lower Humidity")
        self.valves.setValves(self.r2)
        self.compressor.setCompressor(self.r2)
        self.water_pump.setWaterPump(self.r2)

    def startR3(self):
        print("Starting routine: 3, Raise Humidity")
        self.valves.setValves(self.r3)
        self.compressor.setCompressor(self.r3)
        self.water_pump.setWaterPump(self.r3)

    def startR4(self):
        print("Starting routine: 4, Raise Oxygen")
        self.valves.setValves(self.r4)
        self.compressor.setCompressor(self.r4)
        self.water_pump.setWaterPump(self.r4)

    def startR5(self):
        print("Starting routine: 5, Air Cycle")
        self.valves.setValves(self.r5)
        self.compressor.setCompressor(self.r5)
        self.water_pump.setWaterPump(self.r5)