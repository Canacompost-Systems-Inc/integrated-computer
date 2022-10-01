
class Config(object):
    # Flask configuration - note that "from_object() loads only the uppercase attributes of the module/class"
    TESTING = True

    MCU_BAUD_RATE = 9600
    MCU_SERIAL_PORT = '/dev/tty.usbmodem14101'

    # This needs to map {location -> {device_id -> (sensor_type_name/actuator_type_name, device_friendly_name)}}
    # The device_ids need to be unique across locations (since this is used to send and receive messages from MCU)
    DEVICE_MAP = {
        'SharedAirLoop': {
            'c0': ('SHT40', 'SharedTempHumiditySensor'),
            'c1': ('SCD41', 'SharedCO2TempHumiditySensor'),
            'c2': ('IPC10100', 'SharedTempPressureSensor'),
            'e0': ('RotaryDiverterValve1To6', 'RotaryDiverterValveFromSharedAir'),
            'e1': ('RotaryDiverterValve6To1', 'RotaryDiverterValveToSharedAir'),
            'e7': ('FlapDiverterValve', 'FlapDiverterValveSensorLoopBypass'),
            'e8': ('FlapDiverterValve', 'FlapDiverterValveRadiatorBypass'),
            'e9': ('FlapDiverterValve', 'FlapDiverterValveCompostLoopPusher'),
            'ea': ('FlapDiverterValve', 'FlapDiverterValveSensorBoxBypass'),
            'eb': ('DiscreteFlapDiverterValve', 'RegenBlowerStrengthControl'),
            'ec': ('DiscreteFlapDiverterValve', 'EnvironmentExchangeOut'),
            'f1': ('AirMover', 'RegenBlower'),
        },
        'SharedCompostLoop': {
            'e2': ('RotaryDiverterValve1To6', 'RotaryDiverterValveCompostLoop'),
            'e9': ('FlapDiverterValve', 'FlapDiverterValveCompostLoopPusher'),
        },
        'ShredderStorage': {
            'c3': ('DS18B20', 'SoilTempProbeShredderStorage'),
            'e3': ('ButterflyValve', 'ButterflyValveFromShredderStorage'),
            'ed': ('AirHammerValve', 'AirHammerShredderStorage'),
        },
        'Sieve': {
        },
        'Composter': {
        },
        'Larvae': {
        },
        'Bioreactor1': {
            'c4': ('DS18B20', 'SoilTempProbeBioreactor1'),
            'e4': ('ButterflyValve', 'ButterflyValveFromBioreactor1'),
            'ee': ('AirHammerValve', 'AirHammerBioreactor1'),
        },
        'Bioreactor2': {
            'c5': ('DS18B20', 'SoilTempProbeBioreactor2'),
            'e5': ('ButterflyValve', 'ButterflyValveFromBioreactor2'),
            'ef': ('AirHammerValve', 'AirHammerBioreactor2'),
        },
        'BSFReproduction': {
            'c6': ('DS18B20', 'SoilTempProbeBSFReproduction'),
            'e6': ('ButterflyValve', 'ButterflyValveFromBSFReproduction'),
            'f0': ('AirHammerValve', 'AirHammerBSFReproduction'),
            'f2': ('BSFLight', 'BSFReproductionLight'),
        },
    }
