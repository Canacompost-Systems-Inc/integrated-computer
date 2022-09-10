from flask import current_app
import serial


class MCUPersistent:
    def __init__(self, config_prefix='MCU'):
        self.app = None
        self.config_prefix = config_prefix
        self._serial_connection = None

    def init_app(self, app):
        self.app = app
        self.establish_connection()

        if not hasattr(app, "extensions"):
            app.extensions = {}
        app.extensions[self.config_prefix.lower()] = self

    def establish_connection(self):
        # TODO - uncomment before merging (writing this without the device)
        # self._serial_connection = serial.Serial(
        #     app.config['MCU_SERIAL_PORT'],
        #     app.config['MCU_SERIAL_SPEED'],
        #     timeout=1)
        pass

    def get_mcu(self):
        if not self._serial_connection:
            self.establish_connection()
        return self._serial_connection


def get_mcu():
    return current_app.extensions['mcu'].get_mcu()
