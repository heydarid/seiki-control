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
    INPUT_X = 1
    OUTPUT_X = 2
    INPUT_Y = 3
    OUTPUT_Y = 4
    INPUT_Z = 5
    OUTPUT_Z = 6

class Seiki:
    def __init__(self, com_port):
        self.com_port = com_port
        self.baud_rate = 9600
    def goto_abs(axis, )


com_port = '5'  # subject to change...
baud_rate = 9600
ser = serial.Serial(com_port, baud_rate, timeout=0.5)
writedata = 'AXI' + str(i) + ":GOABS" + " 0"
w_data = (writedata + '\r').encode('utf-8')
r_size = 256
ser.write(w_data)