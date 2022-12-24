from application.model.actuator.binary_on_off_actuator import BinaryOnOffActuator


class OzoneGeneratorActuator(BinaryOnOffActuator):

    @property
    def device_type_name(self) -> str:
        return 'OzoneGenerator'
