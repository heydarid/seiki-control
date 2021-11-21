"""
Project Name    : Python GUI operation program
File Name       : control.py
Purpose         : Controlling the Suruga-Seiki DS102 controller box for a 6-axis
                    motorized stage system.
Creation Date   : 2021-Nov-11
Authors         : D. Heydari

NTT-Mabuchi Group
"""

import serial
import serial.tools.list_ports
from tkinter import *
import control
from control import Seiki
from seikicontrol.control import Axis

root = Tk()
root.title(u'SURUGA-SEIKI STAGE CONTROL PROGRAM')
root.geometry('1000x300')
Stage = control.Seiki()

# Axis selection
axis_frame = Frame(root)
axis_frame.pack(fill="x")
Label(axis_frame, text=u'Axis control:  ', font='Helvetica 15').pack(side=LEFT)
axisChoice = IntVar()
for axis in Axis:
    btn = Radiobutton(axis_frame, text=axis.name, activebackground="red", variable=axisChoice, value=axis.value,
                        indicatoron='False', borderwidth=3, font='Helvetica 10')

    btn.pack(side=LEFT, padx=4, pady=4)

# Speed selection
speed_frame = Frame(root)
speed_frame.pack(fill="x")
Label(speed_frame, text=u'Speed setting: ', font='Helvetica 15').pack(side=LEFT)
speedSet = IntVar()
for speed in range(10):
    btnSpeed = Radiobutton(speed_frame, text=str(speed), activebackground="red", variable=speedSet, value=speed, 
                            indicatoron='False', borderwidth=3, font='Helvetica 10')
    btnSpeed.pack(side=LEFT, padx=4, pady=4)

# Absolute position


# Execute
def options():
    Stage.set_speed(axisChoice.get(), speedSet.get())
Button(root, text="EXECUTE",  font='Helvetica 10', width=10, height=2, command=options).place(anchor='center', relx=0.5, rely=0.85)


# emergency stop  (WIP)
xOct, yOct = 25, 25
from math import sin, cos, pi
points = []
for k in range(1,9):
    x0 = xOct * ( cos(2*k*pi / 8 + pi / 8) + 1 ) 
    y0 = yOct * ( sin(2*k*pi / 8 + pi / 8) + 1 )
    points.append(x0)
    points.append(y0)
points = tuple(points)
stop = Canvas(root, width=50, height=50)
stop.create_polygon(points, smooth=False, fill='red', outline = 'black')
stop.create_text(xOct, yOct, text='STOP!', fill="white", font=('Helvetica 10 bold'))
stop.place(anchor='se', relx=1.0, rely=1.0)



root.mainloop()