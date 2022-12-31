
class Config(object):
    # Flask configuration - note that "from_object() loads only the uppercase attributes of the module/class"
    TESTING = True

    MCU_BAUD_RATE = 9600
    MCU_SERIAL_PORT = '/dev/tty.usbmodem14101'

    # This needs to map {location -> {device_id -> (sensor_type_name/actuator_type_name, device_friendly_name)}}
    # The device_ids need to be unique across locations (since this is used to send and receive messages from MCU)
    DEVICE_MAP = {
        'AirLoop': {
            'c0': ('SHT40', 'SharedTempHumiditySensor'),
            'c1': ('SCD41', 'SharedCO2TempHumiditySensor'),
            'c2': ('IPC10100', 'SharedTempPressureSensor'),
            'c7': ('YFS201', 'SharedFlowRateSensor'),
            'c8': ('SEN0441', 'SharedH2Sensor'),
            'c9': ('SEN0321', 'SharedOzoneSensor'),
            'e0': ('RotaryDiverterValve1To6', 'RotaryDiverterValveFromAirLoop'),
            'e1': ('RotaryDiverterValve6To1', 'RotaryDiverterValveToAirLoop'),
            'e7': ('FlapDiverterValve', 'FlapDiverterValveSensorLoopBypass'),
            'e8': ('FlapDiverterValve', 'FlapDiverterValveRadiatorBypass'),
            'ea': ('FlapDiverterValve', 'FlapDiverterValveSensorBoxBypass'),
            'eb': ('DiscreteFlapDiverterValve', 'EnvironmentExchangeOut'),
            'ec': ('DiscreteFlapDiverterValve', 'EnvironmentExchangeIn'),
            'f1': ('AirMover', 'RegenBlower'),
            'f4': ('DiscreteFlapDiverterValve', 'RegenBlowerOutputStrengthModerator'),
            'f3': ('OzoneGenerator', 'OzoneGenerator'),
        },
        'CompostLoop': {
            'e2': ('RotaryDiverterValve1To6', 'RotaryDiverterValveCompostLoop'),
        },
        'ShredderStorage': {
            'c3': ('DS18B20', 'SoilTempProbeShredderStorage'),
            'e3': ('ButterflyValve', 'ButterflyValveFromShredderStorage'),
            'ed': ('AirHammerValve', 'AirHammerShredderStorage'),
            'f5': ('HeaterRelay', 'HeaterRelayShredderStorage'),
            'f6': ('WaterPumpRelay', 'WaterPumpRelayShredderStorage'),
        },
        'Bioreactor1': {
            'c4': ('DS18B20', 'SoilTempProbeBioreactor1'),
            'e4': ('ButterflyValve', 'ButterflyValveFromBioreactor1'),
            'ee': ('AirHammerValve', 'AirHammerBioreactor1'),
            'f7': ('HeaterRelay', 'HeaterRelayBioreactor1'),
            'f8': ('WaterPumpRelay', 'WaterPumpRelayBioreactor1'),
        },
        'Bioreactor2': {
            'c5': ('DS18B20', 'SoilTempProbeBioreactor2'),
            'e5': ('ButterflyValve', 'ButterflyValveFromBioreactor2'),
            'ef': ('AirHammerValve', 'AirHammerBioreactor2'),
            'f9': ('HeaterRelay', 'HeaterRelayBioreactor2'),
            'fa': ('WaterPumpRelay', 'WaterPumpRelayBioreactor2'),
        },
        'BSFReproduction': {
            'c6': ('DS18B20', 'SoilTempProbeBSFReproduction'),
            'e6': ('ButterflyValve', 'ButterflyValveFromBSFReproduction'),
            'f0': ('AirHammerValve', 'AirHammerBSFReproduction'),
            'f2': ('BSFLight', 'BSFReproductionLight'),
            'fb': ('HeaterRelay', 'HeaterRelayBSFReproduction'),
            'e9': ('WaterPumpRelay', 'WaterPumpRelayBSFReproduction'),
        },
        'Sieve': {
        },
    }

    # List of device_ids for sensors that are in the air loop but take measurements for containers
    LOCATION_AWARE_SENSORS = ['c0', 'c1', 'c2', 'c8']
