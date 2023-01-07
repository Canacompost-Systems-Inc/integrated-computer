from application.model.actuator.binary_on_off_actuator import BinaryOnOffActuator


class UVCLightActuator(BinaryOnOffActuator):

    @property
    def device_type_name(self) -> str:
        return 'UVCLight'
