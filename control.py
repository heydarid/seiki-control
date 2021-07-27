"""
Project Name    : Python sample program
File Name       : control
Purpose         : Controlling the Suruga-Seiki DS102 controller box.
Creation Date   : 2021-July-27
Authors         : D. Heydari and M. Catuneanu

NTT-Mabuchi Group
"""

import serial



com_port = '5'  # subject to change...
baud_rate = 9600
ser = serial.Serial(com_port, baud_rate, timeout=0.5)
writedata = 'AXI' + str(i) + ":GOABS" + " 0"
w_data = (writedata + '\r').encode('utf-8')
r_size = 256
ser.write(w_data)