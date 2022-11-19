from application.mcu.actuator.binary_on_off_actuator import BinaryOnOffActuator


class BSFLightActuator(BinaryOnOffActuator):

    @property
    def device_type_name(self) -> str:
        return 'BSFLight'
