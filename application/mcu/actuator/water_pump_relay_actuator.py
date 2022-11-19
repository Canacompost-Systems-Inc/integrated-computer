from application.mcu.actuator.binary_open_close_actuator import BinaryOpenCloseActuator


class WaterPumpRelayActuator(BinaryOpenCloseActuator):

    @property
    def device_type_name(self) -> str:
        return 'WaterPumpRelay'
