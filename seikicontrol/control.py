"""
Project Name    : Python root control program
File Name       : control.py
Purpose         : Controlling the Suruga-Seiki DS102 controller box for a 6-axis
                    motorized stage system.
Creation Date   : 2021-July-27
Authors         : D. Heydari and M. Catuneanu

NTT-Mabuchi Group
"""

from os import device_encoding
import serial
from enum import Enum
from enum import IntEnum

"""
Conventions:
    Z: optic axis (propagation direction)
    X: in plane of table
    Y: out of plane of table
"""

class Axis(IntEnum):
    INPUT_Z = 1
    OUTPUT_Z = 2
    INPUT_Y = 3
    OUTPUT_Y = 4
    INPUT_X = 5
    OUTPUT_X = 6

class Units(IntEnum):
    PULSE = 0
    UM = 1
    MM = 2
    DEG = 3
    MRAD = 4

class Seiki:
    def __init__(self, com_port=5):
        self.com_port = 'COM' + str(com_port)
        self.baud_rate = 9600  # common
        self.ser = serial.Serial(self.com_port, self.baud_rate, timeout=0.5)

    # Action
    def serial_write_read(self, write_data):
        self.ser.write(write_data)
        # print('Tx: ' + write_data.strip().decode("utf-8"))
        read_data = self.ser.read_until(size=256)
        # print('Rx: ' + read_data.strip().decode("utf-8"))
        return read_data

    def set_speed(self, axis, selection):
        if selection > 9:
            print("ERROR: Speed table selection must be an integer between 0 and 9.")
        writedata = 'AXI' + str(axis) + ':SELSP ' + str(selection)
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

    def jog(self, axis, data, dir='CW'):
        writedata = 'AXI' + str(axis) + ":PULS " + str(int(data))
        writedata += ':GO ' + str(dir) + ':DW'
        w_data = (writedata + '\r').encode('utf-8')
        self.serial_write_read(w_data)

    def set_units(self, axis, unit):
        writedata = 'AXI' + str(axis) + ':UNIT ' + str(unit)
        w_data = (writedata + '\r').encode('utf-8')
        self.serial_write_read(w_data)

    # Parameter query
    @property
    def identify(self):
        writedata = '*IDN?'
        w_data = (writedata + '\r').encode('utf-8')
        return self.serial_write_read(w_data)

    def _get_position(self, axis):
        writedata = 'AXI' + str(axis) + ':POS?'
        w_data = (writedata + '\r').encode('utf-8')
        return self.serial_write_read(w_data)

    def _get_speed(self, axis):
        writedata = 'AXI' + str(axis) + ':SELSP?'
        w_data = (writedata + '\r').encode('utf-8')
        return self.serial_write_read(w_data)

    def _get_units(self, axis):
        writedata = 'AXI' + str(axis) + ':UNIT?'
        w_data = (writedata + '\r').encode('utf-8')
        return self.serial_write_read(w_data)

    def _get_driver_division(self, axis):
        writedata = 'AXI' + str(axis) + ':DRDIV?'
        w_data = (writedata + '\r').encode('utf-8')
        idx = int(self.serial_write_read(w_data).strip().decode("utf-8"))
        selection = ['1:1', '1:2', '1:2.5', '1:4', 
                     '1:5', '1:8', '1:10', '1:20'
                     '1:25', '1:40', '1:50', '1:80'
                     '1:100', '1:125', '1:200', '1:250']
        return selection[idx]
    
    def _get_resolution(self, axis):
        # This is the travel distance per pulse, a function
        # of the driver division setting.
        writedata = 'AXI' + str(axis) + ':RESOLUT?'
        w_data = (writedata + '\r').encode('utf-8')
        return self.serial_write_read(w_data)
    
    def _get_pulse_setting(self, axis):
        writedata = 'AXI' + str(axis) + ':PULS?'
        w_data = (writedata + '\r').encode('utf-8')
        return self.serial_write_read(w_data)
    
    def _verify_home(self, axis):  # (0), 1: (un)detected
        writedata = 'AXI' + str(axis) + ':HOME?'
        w_data = (writedata + '\r').encode('utf-8')
        return self.serial_write_read(w_data)
    
    def _verify_all_moving(self):
        writedata = 'MOTIONAll?'
        w_data = (writedata + '\r').encode('utf-8')
        return self.serial_write_read(w_data)
