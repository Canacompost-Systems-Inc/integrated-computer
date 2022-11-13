
class Config(object):
    # Flask configuration - note that "from_object() loads only the uppercase attributes of the module/class"
    TESTING = True

    MCU_BAUD_RATE = 9600
    MCU_SERIAL_PORT = '/dev/tty.usbmodem14101'

    # This needs to map {location -> {device_id -> (sensor_type_name/actuator_type_name, device_friendly_name)}}
    # The device_ids need to be unique across locations (since this is used to send and receive messages from MCU)
    DEVICE_MAP = {
        'BIOREACTOR1': {
            'e1': ('Valve', 'Bioreactor1InValve'),
            'c3': ('DS18B20', 'Bioreactor1SoilTempProbe'),
        },
        'SHARED': {
            'c0': ('SHT40', 'SharedTempHumiditySensor'),
            'c1': ('SCD41', 'SharedCO2TempHumiditySensor'),
            'c2': ('IPC10100', 'SharedTempPressureSensor'),
            'e0': ('Compressor', 'SharedCompressor'),
            'e2': ('Valve', 'SharedEnvExchangeInValve'),
            'e3': ('Valve', 'SharedEnvExchangeBypassValve'),
            'e4': ('Valve', 'SharedEnvExchangeOutValve'),
            'e5': ('Valve', 'SharedSensorLoopBypassValve'),
            'e6': ('Valve', 'SharedSensorLoopStartValve'),
        },
    }

