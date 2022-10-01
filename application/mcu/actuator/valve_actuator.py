from application.mcu.actuator.boolean_actuator import BooleanActuator


class ValveActuator(BooleanActuator):

    @property
    def device_type_name(self) -> str:
        return 'Valve'
