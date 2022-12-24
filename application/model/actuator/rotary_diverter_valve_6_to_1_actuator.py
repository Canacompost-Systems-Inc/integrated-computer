from application.model.actuator.rotary_diverter_valve_actuator import RotaryDiverterValveActuator


class RotaryDiverterValve6To1Actuator(RotaryDiverterValveActuator):

    @property
    def device_type_name(self) -> str:
        return 'RotaryDiverterValve6To1'
