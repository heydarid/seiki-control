"""
Project Name    : Python root control program
File Name       : control.py
Purpose         : Controlling the Suruga-Seiki DS102 controller box for a 6-axis
                    motorized stage system.
Creation Date   : 2021-July-27
Authors         : D. Heydari and M. Catuneanu

NTT-Mabuchi Group
"""
__all__ = ["Axis", "Units", "Attribute", "Seiki"]

from os import device_encoding, write
import serial
from enum import Enum
from enum import IntEnum
from textwrap import wrap
from time import sleep

"""
Conventions:
    Z: optic axis (propagation direction)
    X: in plane of table
    Y: out of plane of table
"""

from aenum import AutoNumberEnum
class Axis(AutoNumberEnum):
    _init_ = 'value text'
    INPUT_Z =  1, 'AXI1'
    OUTPUT_Z = 2, 'AXI2'
    INPUT_Y =  3, 'AXI3'
    OUTPUT_Y = 4, 'AXI4'
    INPUT_X =  5, 'AXI5'
    OUTPUT_X = 6, 'AXI6'

class Units(IntEnum):
    PULSE = 0
    UM = 1
    MM = 2
    DEG = 3
    MRAD = 4

class Command(Enum):
    IDN = '*IDN'
    SPD = 'SELSP'
    POS = 'POS'
    UNT = 'UNIT'
    GOA = 'GOABS'
    DRD = 'DRDIV'
    RES = 'RESOLUT'
    JOG = 'PULS'
    STOP = 'STOP 0'
    ESTOP = 'STOP 1'
    HOME = 'HOME'
    MOVING = 'MOTIONAll'

class Controller:
    MAXCHAR = 100
    def __init__(self, com_port=5):
        self.com_port = 'COM' + str(com_port)
        self.baud_rate = 38400
        self.ser = serial.Serial(self.com_port, self.baud_rate, timeout=0.5)

    def _serial_write_read(self, write_data):
        self.ser.write(write_data)
        return self.ser.read_until()

    def _clean(self, output):
        return output.decode('utf-8').split()

    def query(self, axes, attributes):
        query = [(i, j) for i in axes for j in attributes]
        write = ''.join([m[0].text + ':' + str(m[1].value) + '?' + '\r' for m in query])
        if len(write) > Controller.MAXCHAR: return query, self._multi_write(write)
        return query, self._clean(self._serial_write_read(write.encode('utf-8')))

    def _multi_write(self, write):
        multiwrite = wrap(write, Controller.MAXCHAR, replace_whitespace=False)
        multiwrite = [m + '\r' for m in multiwrite]
        result = []
        for m in multiwrite:
            result.append(self._serial_write_read(( m.split('\n')[0]).encode('utf-8') ))
            sleep(0.2)
        return [item for sublist in [self._clean(r) for r in result] for item in sublist]

    def set(self, axis, attribute, value):  # one axis and attribute at a time
        write = axis.text + ':' + str(attribute.value) + ' ' + str(value) + '\r'
        print('Tx: ', write)
        return self._serial_write_read(write.encode('utf-8'))

    def jog(self, axis, data, dir='CW'):
        writedata = (axis.text + ":PULS " + str(int(data)) + \
            ':GO ' + str(dir) + ':DW' + '\r').encode('utf-8')
        self._serial_write_read(writedata)

    def emergency_stop(self):
        writedata = ('STOP 0' + '\r').encode('utf-8')
        self._serial_write_read(writedata)

    def slow_stop(self):
        writedata = ('STOP 1' + '\r').encode('utf-8')
        self._serial_write_read(writedata)

    # Parameter query
    def identify(self):
        writedata = ('*IDN?' + '\r').encode('utf-8')
        return self._serial_write_read(writedata)

    def _verify_home(self, axis):  # (0), 1: (un)detected
        writedata = axis.text + ':HOME?'
        w_data = (writedata + '\r').encode('utf-8')
        return self._serial_write_read(w_data)
    
    def _verify_all_moving(self):
        writedata = 'MOTIONAll?'
        w_data = (writedata + '\r').encode('utf-8')
        return self._serial_write_read(w_data)