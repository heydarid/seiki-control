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
from control import *

root = Tk()
root.title(u'SURUGA-SEIKI STAGE CONTROL PROGRAM')
root.geometry('500x600')

# Axis selection
axisSelect = Label(text=u'Axis control')
axisSelect.place(x=50, y=30)

axisChoice = StringVar()

axisChoice = StringVar()

btnXin = Radiobutton(text='X IN', activebackground="red", variable=axisChoice, value=Axis.INPUT_X,
                        indicatoron='False', borderwidth=3, padx=5, pady=5, font='Helvetica 10')
x0, DX = 50, 70
btnXin.place(x=x0, y=50)

btnYin = Radiobutton(text='Y IN', activebackground="red", variable=axisChoice, value=Axis.INPUT_Y,
                        indicatoron='False', borderwidth=3, padx=5, pady=5, font='Helvetica 10')
btnYin.place(x=x0+DX, y=50)

btnYin = Radiobutton(text='Z IN', activebackground="red", variable=axisChoice, value=Axis.INPUT_Z,
                        indicatoron='False', borderwidth=3, padx=5, pady=5, font='Helvetica 10')
btnYin.place(x=x0+2*DX, y=50)

btnYin = Radiobutton(text='X OUT', activebackground="red", variable=axisChoice, value=Axis.OUTPUT_X,
                        indicatoron='False', borderwidth=3, padx=5, pady=5, font='Helvetica 10')
btnYin.place(x=x0+3*DX, y=50)

btnYin = Radiobutton(text='Y OUT', activebackground="red", variable=axisChoice, value=Axis.OUTPUT_Y,
                        indicatoron='False', borderwidth=3, padx=5, pady=5, font='Helvetica 10')
btnYin.place(x=x0+4*DX, y=50)

btnYin = Radiobutton(text='Z OUT', activebackground="red", variable=axisChoice, value=Axis.OUTPUT_Z,
                        indicatoron='False', borderwidth=3, padx=5, pady=5, font='Helvetica 10')
btnYin.place(x=x0+5*DX, y=50)



root.mainloop()