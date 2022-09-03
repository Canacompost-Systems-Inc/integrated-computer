import struct
import serial
import struct
from service.model.routine import *

class MCUService():

    SAMPLE_REQ = "S"
    #SAMPLE_BYTES = 0x01 22 33 44 55 03
    # STX = 0x01
    # Device id = 0x22
    # First float val = 22.5 (0x41b40000)
    # Second float val = 10.0 (0x41200000)
    # Third float val = 1.25 (0x3fa00000)
    SAMPLE_BYTES = 0x012241b40000412000003fa0000003

    def __init__(self):
        print("Hello world")

    def decode(self, hex_str):
        print("Decoding...")

        #print(hex(self.SAMPLE_BYTES))
        #str_input = hex(self.SAMPLE_BYTES)

        print(hex_str[0:8])

        val_1 = struct.unpack('!f', bytes.fromhex(hex_str[0:8]))[0]
        val_2 = struct.unpack('!f', bytes.fromhex(hex_str[8:16]))[0]
        val_3 = struct.unpack('!f', bytes.fromhex(hex_str[16:24]))[0]

        print(val_1)
        print(val_2)
        print(val_3)

    def poll(self):
        print("Polling...")
        serial_speed = 9600
        serial_port = '/dev/tty.usbmodem14301'
        ser = serial.Serial(serial_port, serial_speed, timeout = 1)

        did = ''
        data = ''
        state = 0

        while True:
            byte = ser.read()
            
            # Idle
            if state == 0:
                if byte == b'\x02':
                    state = 1
                else:
                    ser.write(b'\x73')

            # Identify
            elif state == 1:
                if byte:
                    did = byte.hex()
                    state = 2
            
            # Read
            elif state == 2:
                if byte == b'\x03':
                    # print(did, struct.unpack('!f', bytes.fromhex(data))[0]) # Decodes data (float)
                    print(did, data)

                    self.decode(str(data))
                elif byte:
                    data = byte.hex() + data

