
class Config(object):
    # Flask configuration - note that "from_object() loads only the uppercase attributes of the module/class"
    TESTING = False

    MCU_SERIAL_SPEED = 9600
    MCU_SERIAL_PORT = '/dev/tty.usbmodem14201'

