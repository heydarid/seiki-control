"""
Project Name    : Python sample program
File Name       : control
Purpose         : Controlling the Suruga-Seiki DS102 controller box.
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
    0. Recieve data properly
    1. Write a function that jogs motor
    2. Ensure that goto_abs WAITS until desired position is achieved
    3. Maximize throughput function
"""
class Seiki:
    def __init__(self, com_port=5):
        self.com_port = 'COM' + str(com_port)
        self.baud_rate = 9600  # common
        self.ser = serial.Serial(self.com_port, self.baud_rate, timeout=0.5)
    def speed(self, axis, selection):
        if selection > 9:
            print("ERROR: Speed table selection must be an integer between 0 and 9.")
        writedata = 'SELSP ' + str(selection)
        w_data = (writedata + '\r').encode('utf-8')
        self.ser.write(w_data)
    def goto_abs(self, axis, pos):
        writedata = 'AXI' + str(axis) + ":GOABS " + str(int(pos))
        w_data = (writedata + '\r').encode('utf-8')
        self.ser.write(w_data)

    # Parameter query
    def _get_position(self):
        writedata = 'POS?'
        w_data = (writedata + '\r').encode('utf-8')
        self.ser.write(w_data)