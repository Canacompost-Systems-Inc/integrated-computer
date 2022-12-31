from abc import ABCMeta

from application.model.base_device import BaseDevice


class BaseSensor(BaseDevice, metaclass=ABCMeta):

    @property
    def device_category(self) -> str:
        return 'sensor'
