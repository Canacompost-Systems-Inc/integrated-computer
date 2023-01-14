from flask import current_app
import logging
import serial
import time


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
        if not self.app.config['TESTING']:
            self._serial_connection = serial.Serial(
                self.app.config['MCU_SERIAL_PORT'],
                self.app.config['MCU_BAUD_RATE'],
                timeout=5)
            time.sleep(1)

            self.clear_buffers()

    def clear_buffers(self):
        # Get the contents of the input buffer
        buffer = b''
        try:
            buffer = self._serial_connection.read(self._serial_connection.in_waiting())
        except:
            pass
        # Print the contents of the input buffer
        if buffer != b'':
            logging.debug(f"Buffer contents: {buffer}")
            try:
                decoded = bytes.fromhex(buffer).decode('utf-8')
                logging.debug(f"Response from MCU (decoded): {decoded}")
            except Exception:
                pass
        # Clear the buffers
        self._serial_connection.reset_input_buffer()
        self._serial_connection.reset_output_buffer()

    def get_mcu(self):
        if not self._serial_connection:
            self.establish_connection()
        return self._serial_connection


def get_mcu():
    return current_app.extensions['mcu'].get_mcu()
