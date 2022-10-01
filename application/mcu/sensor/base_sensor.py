from abc import ABCMeta
from typing import Dict, List

from application.mcu.base_device import BaseDevice


class BaseSensor(BaseDevice, metaclass=ABCMeta):

    @property
    def device_category(self) -> str:
        return 'sensor'
