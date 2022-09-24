from abc import ABCMeta, abstractmethod
from typing import Dict, List

from application.mcu.base_device import BaseDevice


class BaseActuator(BaseDevice, metaclass=ABCMeta):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._state = None

    @property
    def device_category(self) -> str:
        return 'actuator'

    @property
    def payload_length(self) -> int:
        return 1

    @property
    def measurement_order(self) -> List[str]:
        return ['state']

    @property
    def current_state(self):
        return self._state

    @current_state.setter
    def current_state(self, val):
        self._state = val

    @property
    @abstractmethod
    def possible_states(self) -> Dict[str, bytes]:
        pass

    @property
    @abstractmethod
    def default_state(self) -> str:
        pass
