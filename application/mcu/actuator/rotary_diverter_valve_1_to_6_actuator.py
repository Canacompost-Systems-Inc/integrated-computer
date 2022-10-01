from application.mcu.actuator.multi_6_actuator import Multi6Actuator


class RotaryDiverterValve1To6Actuator(Multi6Actuator):

    @property
    def device_type_name(self) -> str:
        return 'RotaryDiverterValve1To6'
