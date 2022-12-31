from application.model.actuator.binary_open_close_actuator import BinaryOpenCloseActuator


class ButterflyValveActuator(BinaryOpenCloseActuator):

    @property
    def device_type_name(self) -> str:
        return 'ButterflyValve'
