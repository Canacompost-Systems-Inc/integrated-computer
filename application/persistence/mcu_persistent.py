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
        logging.debug(f"Test 1")
        buffer = b''
        try:
            logging.debug(f"Test 2")
            buffer = self._serial_connection.read(self._serial_connection.in_waiting)
            logging.debug(f"Test 3")
        except Exception as e:
            logging.debug(f"Encountered error while reading input buffer: {e}")
        # Print the contents of the input buffer
        logging.debug(f"Test 4")
        if buffer != b'':
            logging.debug(f"Test 5")
            logging.debug(f"Buffer contents: {buffer}")
            try:
                decoded = bytes.fromhex(buffer).decode('utf-8')
                logging.debug(f"Response from MCU (decoded): {decoded}")
            except Exception:
                pass
        # Clear the buffers
        logging.debug(f"Test 6")
        self._serial_connection.reset_input_buffer()
        logging.debug(f"Test 7")
        self._serial_connection.reset_output_buffer()
        logging.debug(f"Test 8")

    def get_mcu(self):
        if not self._serial_connection:
            self.establish_connection()
        return self._serial_connection


def get_mcu():
    return current_app.extensions['mcu'].get_mcu()
