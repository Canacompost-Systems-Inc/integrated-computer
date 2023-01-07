from typing import Optional


class SharedAirSensors:
    def __init__(self,
                 flowrate: Optional[float] = None,
                 o3: Optional[float] = None,
                 ):
        self.flowrate = flowrate
        self.o3 = o3
