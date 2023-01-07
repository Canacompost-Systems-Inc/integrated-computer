from dataclasses import dataclass
from typing import Optional


@dataclass
class Action:
    """Class for setting an actuator to a particular state or reading a sensor value"""
    device_id: str
    set_to_value: Optional[str] = None  # If None, this is a sensor that needs to be read
