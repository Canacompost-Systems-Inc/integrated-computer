
class Config(object):
    # Flask configuration - note that "from_object() loads only the uppercase attributes of the module/class"
    TESTING = True

    MCU_BAUD_RATE = 9600
    MCU_SERIAL_PORT = '/dev/tty.usbmodem14201'
