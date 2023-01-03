
class Config(object):
    # Flask configuration - note that "from_object() loads only the uppercase attributes of the module/class"
    TESTING = True

    MCU_BAUD_RATE = 9600
    MCU_SERIAL_PORT = '/dev/tty.usbmodem14101'

    # TODO - contact Kaan to update the dashboard pane of the UI to reflect the new sensor measurements (the chambers one works)

    # This needs to map {location -> {device_id -> (sensor_type_name/actuator_type_name, device_friendly_name)}}
    # The device_ids need to be unique across locations (since this is used to send and receive messages from MCU)
    DEVICE_MAP = {
        'AirLoop': {
            'c0': ('SHT40', 'Shared Temp Humidity Sensor'),
            'c1': ('SCD41', 'Shared CO2 Temp Humidity Sensor'),
            'c2': ('IPC10100', 'Shared Temp Pressure Sensor'),
            'c7': ('YFS201', 'Shared Flow Rate Sensor'),
            'c8': ('SEN0441', 'Shared H2 Sensor'),
            'c9': ('SEN0321', 'Shared Ozone Sensor'),
            'e0': ('RotaryDiverterValve1To6', 'Rotary Diverter Valve From Air Loop'),
            'e1': ('RotaryDiverterValve6To1', 'Rotary Diverter Valve To Air Loop'),
            'e7': ('FlapDiverterValve', 'Flap Diverter Valve Sensor Loop Bypass'),
            'e8': ('FlapDiverterValve', 'Flap Diverter Valve Radiator Bypass'),
            'ea': ('FlapDiverterValve', 'Flap Diverter Valve Sensor Box Bypass'),
            'eb': ('DiscreteFlapDiverterValve', 'Environment Exchange Out'),
            'ec': ('DiscreteFlapDiverterValve', 'Environment Exchange In'),
            'f1': ('AirMover', 'Regen Blower'),
            # TODO - f4 DiscreteFlapDiverterValve has been removed, and is now a UVC light switch
            # TODO - also make sure to update the calls to f4 in the actions
            # 'f4': ('DiscreteFlapDiverterValve', 'Regen Blower Output Strength Moderator'),
            'f4': ('UVCLight', 'UVC Light'),
            'f3': ('OzoneGenerator', 'Ozone Generator'),
        },
        'CompostLoop': {
            'e2': ('RotaryDiverterValve1To6', 'Rotary Diverter Valve Compost Loop'),
        },
        'ShredderStorage': {
            'c3': ('DS18B20', 'Soil Temp Probe Shredder Storage'),
            'e3': ('ButterflyValve', 'Butterfly Valve From Shredder Storage'),
            'ed': ('AirHammerValve', 'Air Hammer Shredder Storage'),
            'f5': ('HeaterRelay', 'Heater Relay Shredder Storage'),
            'f6': ('WaterPumpRelay', 'Water Pump Relay Shredder Storage'),
        },
        'Bioreactor1': {
            'c4': ('DS18B20', 'Soil Temp Probe Bioreactor1'),
            'e4': ('ButterflyValve', 'Butterfly Valve From Bioreactor1'),
            'ee': ('AirHammerValve', 'Air Hammer Bioreactor1'),
            'f7': ('HeaterRelay', 'Heater Relay Bioreactor1'),
            'f8': ('WaterPumpRelay', 'Water Pump Relay Bioreactor1'),
        },
        'Bioreactor2': {
            'c5': ('DS18B20', 'Soil Temp Probe Bioreactor2'),
            'e5': ('ButterflyValve', 'Butterfly Valve From Bioreactor2'),
            'ef': ('AirHammerValve', 'Air Hammer Bioreactor2'),
            'f9': ('HeaterRelay', 'Heater Relay Bioreactor2'),
            'fa': ('WaterPumpRelay', 'Water Pump Relay Bioreactor2'),
        },
        'BSFReproduction': {
            'c6': ('DS18B20', 'Soil Temp Probe BSFReproduction'),
            'e6': ('ButterflyValve', 'Butterfly Valve From BSFReproduction'),
            'f0': ('AirHammerValve', 'Air Hammer BSFReproduction'),
            'f2': ('BSFLight', 'BSFReproduction Light'),
            'fb': ('HeaterRelay', 'Heater Relay BSFReproduction'),
            'e9': ('WaterPumpRelay', 'Water Pump Relay BSFReproduction'),
        },
        'Sieve': {
        },
    }

    # List of device_ids for sensors that are in the air loop but take measurements for containers
    LOCATION_AWARE_SENSORS = ['c0', 'c1', 'c2', 'c8']
