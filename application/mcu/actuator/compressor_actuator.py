from application.mcu.actuator.boolean_actuator import BooleanActuator


class CompressorActuator(BooleanActuator):

    @property
    def device_type_name(self) -> str:
        return 'Compressor'
