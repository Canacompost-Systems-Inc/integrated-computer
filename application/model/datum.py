from dataclasses import dataclass, field
from datetime import datetime

from application.model.base_device import BaseDevice
from application.model.measurement.base_measurement import BaseMeasurement


@dataclass
class Datum:
    """Class for an instance of a measurement by a device"""
    device: BaseDevice
    measurement: BaseMeasurement
    timestamp: datetime = field(default_factory=datetime.utcnow)
