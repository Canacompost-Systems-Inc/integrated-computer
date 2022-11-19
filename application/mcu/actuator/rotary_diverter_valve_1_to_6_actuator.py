from application.mcu.actuator.rotary_diverter_valve_actuator import RotaryDiverterValveActuator


class RotaryDiverterValve1To6Actuator(RotaryDiverterValveActuator):

    @property
    def device_type_name(self) -> str:
        return 'RotaryDiverterValve1To6'
