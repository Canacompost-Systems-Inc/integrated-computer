from application.mcu.actuator.discrete_step_degree_10_actuator import DiscreteStepDegree10Actuator


class ButterflyValveActuator(DiscreteStepDegree10Actuator):

    @property
    def device_type_name(self) -> str:
        return 'ButterflyValve'
