"""
Project Name    : Python sample program
File Name       : control.py
Purpose         : Controlling the Suruga-Seiki DS102 controller box for a 6-axis
                    motorized stage system.
Creation Date   : 2021-July-27
Authors         : D. Heydari and M. Catuneanu

NTT-Mabuchi Group
"""

import serial
from enum import Enum
from enum import IntEnum

class Axis(IntEnum):
    INPUT_Z = 1
    OUTPUT_Z = 2
    INPUT_Y = 3
    OUTPUT_Y = 4
    INPUT_X = 5
    OUTPUT_X = 6
"""
TODO:
    0. Use the above enums for axis control
    1. Write a function that jogs motor
    2. Ensure that goto_abs WAITS until desired position is achieved
    3. Maximize throughput function
"""
class Seiki:
    def __init__(self, com_port=5):
        self.com_port = 'COM' + str(com_port)
        self.baud_rate = 9600  # common
        self.ser = serial.Serial(self.com_port, self.baud_rate, timeout=0.5)

    # Action
    def serial_write_read(self, write_data):
        self.ser.write(write_data)
        print('Tx: ' + write_data.strip().decode("utf-8"))

        read_data = self.ser.read_until(size=256)
        print('Rx: ' + read_data.strip().decode("utf-8"))

        return read_data

    def speed(self, axis, selection):
        if selection > 9:
            print("ERROR: Speed table selection must be an integer between 0 and 9.")
        writedata = 'SELSP ' + str(selection)
        w_data = (writedata + '\r').encode('utf-8')
        self.serial_write_read(w_data)

    def goto_abs(self, axis, pos):
        writedata = 'AXI' + str(axis) + ":GOABS " + str(int(pos))
        w_data = (writedata + '\r').encode('utf-8')
        self.serial_write_read(w_data)

    def emergency_stop(self):
        writedata = 'STOP 0'
        w_data = (writedata + '\r').encode('utf-8')
        self.serial_write_read(w_data)

    def slow_stop(self):
        writedata = 'STOP 1'
        w_data = (writedata + '\r').encode('utf-8')
        self.serial_write_read(w_data)

    def jog(self, axis, divisions):
        pass

    def drive_direction(self):
        # this needs to act like a toggle switch.
        pass

    # Parameter query
    @property
    def identify(self):
        writedata = '*IDN?'
        w_data = (writedata + '\r').encode('utf-8')
        self.serial_write_read(w_data)

    def _get_position(self, axis):
        writedata = 'AXI' + str(axis) + ':POS?'
        w_data = (writedata + '\r').encode('utf-8')
        self.serial_write_read(w_data)

    def _get_speed(self, axis):
        writedata = 'AXI' + str(axis) + 'SELSP?'
        w_data = (writedata + '\r').encode('utf-8')
        self.serial_write_read(w_data)

    def _get_units(self, axis):
        writedata = 'AXI' + str(axis) + 'UNIT?'
        w_data = (writedata + '\r').encode('utf-8')
        self.serial_write_read(w_data)