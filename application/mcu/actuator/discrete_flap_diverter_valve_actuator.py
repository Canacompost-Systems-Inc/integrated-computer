from application.mcu.actuator.discrete_step_percentage_21_actuator import DiscreteStepPercentage21Actuator


class DiscreteFlapDiverterValveActuator(DiscreteStepPercentage21Actuator):

    @property
    def device_type_name(self) -> str:
        return 'DiscreteFlapDiverterValve'
