from typing import Literal, Dict, Optional

from application.controller.dto.machine_state import MachineState
from application.controller.dto.machine_sensors import Sensors
from application.controller.dto.sensors.bioreactor_1_sensors import Bioreactor1Sensors
from application.controller.dto.sensors.bioreactor_2_sensors import Bioreactor2Sensors
from application.controller.dto.sensors.bsf_reproduction_sensors import BSFReproductionSensors
from application.controller.dto.sensors.shared_air_sensors import SharedAirSensors
from application.controller.dto.sensors.shredder_sensors import ShredderSensors
from application.controller.dto.actuators.actuator import Actuator
from application.controller.dto.actuators.options import Options
from application.controller.dto.actuators.type import Type
from application.model.action.action import Action
from application.model.action.action_set import ActionSet
from application.model.routine.advanced_tab_routine import AdvancedTabRoutine
from application.model.routine.routine_step import RoutineStep
from application.service.device_registry_service import DeviceRegistryService
from application.service.mcu_state_tracker_service import MCUStateTrackerService


class DtoTranslatorService:
    """Service for translating to and from the dto objects that the frontend uses."""

    def __init__(self, device_registry_service: DeviceRegistryService):
        self.device_registry_service = device_registry_service

    def _construct_actuator_dto(self, device_id: str, state_value: str):

        device = self.device_registry_service.get_device(device_id)

        # Boolean values need to be true/false and not open/close and on/off
        remap_state_value = {
            'open': 'true',
            'close': 'false',
            'on': 'true',
            'off': 'false',
            'divert': 'true',
            'through': 'false',
        }
        val = remap_state_value.get(state_value, state_value)

        display_type = Type.SWITCH
        if device.device_type_name in [
            'RotaryDiverterValve1To6',
            'RotaryDiverterValve6To1'
        ]:
            display_type = Type.RADIO
        elif device.device_type_name == 'DiscreteFlapDiverterValve':
            display_type = Type.RANGE

        options = min = max = step = unit = None
        if display_type == Type.RADIO:
            options = []
            for string_value in device.possible_states.keys():
                options.append(Options(string_value, int(string_value)))
        elif display_type == Type.RANGE:
            # Hard coding this because this only works for the flap diverter valve.
            min = 0
            max = 100
            step = 5
            unit = 'percent'

        return Actuator(
                device_id,
                str(display_type.name),
                device.device_friendly_name,
                val,
                options,
                min,
                max,
                step,
                unit
            )

    def _construct_actuators_dto(self, actuator_states: Dict[str, str]):
        actuators = []
        for device_id, state_value in actuator_states.items():
            actuators.append(self._construct_actuator_dto(device_id, state_value))
        return actuators

    def _construct_location_sensor_dto(self,
                                       measurement_values: Dict[str, str],
                                       location: Literal['AirLoop', 'ShredderStorage', 'Bioreactor1', 'Bioreactor2',
                                                        'BSFReproduction']):

        dto_class = {
            'AirLoop': SharedAirSensors,
            'ShredderStorage': ShredderSensors,
            'Bioreactor1': Bioreactor1Sensors,
            'Bioreactor2': Bioreactor2Sensors,
            'BSFReproduction': BSFReproductionSensors
        }.get(location)

        return dto_class(**{
            measurement_name: float(value) if value is not None else None
            for measurement_name, value
            in measurement_values.items()
        })

    def _construct_sensors_dto(self, latest_measurements: Dict[str, Dict[str, str]]):
        return Sensors(
            self._construct_location_sensor_dto(latest_measurements.get('AirLoop', {}), 'AirLoop'),
            self._construct_location_sensor_dto(latest_measurements.get('ShredderStorage', {}), 'ShredderStorage'),
            self._construct_location_sensor_dto(latest_measurements.get('Bioreactor1', {}), 'Bioreactor1'),
            self._construct_location_sensor_dto(latest_measurements.get('Bioreactor2', {}), 'Bioreactor2'),
            self._construct_location_sensor_dto(latest_measurements.get('BSFReproduction', {}), 'BSFReproduction'),
        )

    def construct_machine_state_dto(self,
                                    actuator_states: Dict[str, str],
                                    latest_measurements: Dict[str, Dict[str, str]]) -> MachineState:
        return MachineState(
            self._construct_actuators_dto(actuator_states),
            self._construct_sensors_dto(latest_measurements)
        )

    def generate_routine_to_set_actuator_state(self,
                                               current_actuator_states: Dict[str, str],
                                               intended_machine_state: MachineState,
                                               ) -> Optional[AdvancedTabRoutine]:
        """Takes in the current actuator state, a mapping of device_id to state value, and the intended machine state
        posted by the frontend, and returns a routine if any actions need to be taken. """

        intended_actuator_states = {}
        for actuator in intended_machine_state.actuators:
            intended_actuator_states[actuator.id] = actuator.value

        required_actions = []
        for device_id, intended_state_value in intended_actuator_states.items():

            device = self.device_registry_service.get_device(device_id)

            # Boolean values need to be true/false and not open/close and on/off
            if 'open' in device.possible_states.keys():
                intended_val = {'true': 'open', 'false': 'close'}.get(intended_state_value)
            elif 'on' in device.possible_states.keys():
                intended_val = {'true': 'on', 'false': 'off'}.get(intended_state_value)
            elif 'divert' in device.possible_states.keys():
                intended_val = {'true': 'divert', 'false': 'through'}.get(intended_state_value)
            else:
                intended_val = intended_state_value

            # Verify that the intended state is a possible state
            if intended_val not in device.possible_states.keys():
                raise RuntimeError(
                    f"Cannot set state of {device.device_friendly_name} ({device_id}) to '{intended_val}' "
                    f"because the possible states are {list(device.possible_states.keys())}")

            # Verify that the intended state is not already set
            if current_actuator_states.get(device_id, None) == intended_val:
                continue

            required_actions.append(Action(device_id, intended_val))

        if len(required_actions) == 0:
            return None

        return AdvancedTabRoutine(steps=[
            RoutineStep(ActionSet(iterable=required_actions), then_wait_n_sec=0)
        ])
