from application.model.actuator.binary_open_close_actuator import BinaryOpenCloseActuator


class HeaterRelayActuator(BinaryOpenCloseActuator):

    @property
    def device_type_name(self) -> str:
        return 'HeaterRelay'
