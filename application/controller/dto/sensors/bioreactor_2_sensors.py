from typing import Optional


class Bioreactor2Sensors:
    def __init__(self,
                 temperature: Optional[float] = None,
                 humidity: Optional[float] = None,
                 co2: Optional[float] = None,
                 pressure: Optional[float] = None,
                 h2: Optional[float] = None,
                 ):
        self.temperature = temperature
        self.humidity = humidity
        self.co2 = co2
        self.pressure = pressure
        self.h2 = h2
