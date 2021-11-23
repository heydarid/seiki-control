"""
Project Name    : Python GUI operation program
File Name       : control.py
Purpose         : Controlling the Suruga-Seiki DS102 controller box for a 6-axis
                    motorized stage system.
Creation Date   : 2021-Nov-11
Authors         : D. Heydari

NTT-Mabuchi Group
"""
from tkinter import *
from control import Seiki
from seikicontrol.control import Axis
from tkinter import ttk
from math import sin, cos, pi

# TODO:
# 1. Units
# 2. Make sure updating of table actually happend AFTER stage stopped moving
# 3. emergency stop button

# main
if __name__ == '__main__':
    root = Tk()
    root.title(u'SURUGA-SEIKI STAGE CONTROL PROGRAM')
    root.geometry('500x500')
    Stage = Seiki()

    # Axis selection
    axis_frame = LabelFrame(root, text="Axis",  font='Helvetica 13', bg='lemon chiffon')
    axis_frame.pack(fill="both")
    axisChoice = IntVar()
    for axis in Axis:
        btn = Radiobutton(axis_frame, text=axis.name, activebackground="red", variable=axisChoice, value=axis.value,
                            indicatoron='False', borderwidth=3, font='Helvetica 10')

        btn.pack(side=LEFT, padx=4, pady=4)

    # Speed selection
    speed_frame = LabelFrame(root, text="Speed",  font='Helvetica 13', bg='azure')
    speed_frame.pack(fill='both')
    speedSet = IntVar()
    for speed in range(10):
        btnSpeed = Radiobutton(speed_frame, text=str(speed), activebackground="red", variable=speedSet, value=speed, 
                                indicatoron='False', borderwidth=3, font='Helvetica 10')
        btnSpeed.pack(side=LEFT, padx=4, pady=4)
    speed_set_button = Button(speed_frame, text='SET')
    speed_set_button.pack(side=RIGHT)
    def speed_set_function(action):
        Stage.set_speed(axisChoice.get(), speedSet.get())
        update_table(axisChoice.get())
    speed_set_button.bind("<Button-1>", speed_set_function)

    # control frame
    control_frame = LabelFrame(root, text="Motion",  font='Helvetica 13', bg='seashell2')
    control_frame.pack(fill=BOTH)
    ## Absolute position
    abs_pos_frame = Frame(control_frame, bg='seashell2', borderwidth=6, relief=RIDGE)
    abs_pos_frame.pack(side=LEFT, padx=15)
    pos_button = Button(abs_pos_frame, text=u'To Pos', font='Helvetica 12 italic')
    pos_button.pack(side=BOTTOM)
    position_desired = Entry(abs_pos_frame, width=15)
    position_desired.pack(side=LEFT)

    ## Jogging
    jog_frame = Frame(control_frame, bg='seashell2', borderwidth=6, relief=RIDGE)
    jog_frame.pack(side=LEFT, padx=15)

    jog_button = Button(jog_frame, text=u'JOG', font='Helvetica 12 italic', wraplength=1)
    jog_button.pack(side=RIGHT)

    direction = StringVar()
    btnCW = Radiobutton(jog_frame, text='CW', activebackground="red", variable=direction, value='CW',
                            indicatoron='False', borderwidth=3, font='Helvetica 10')
    btnCW.pack(side=TOP, padx=4, pady=4)
    jog_amount = Entry(jog_frame, width=15)
    jog_amount.pack(side=TOP)
    btnCCW = Radiobutton(jog_frame, text='CCW', activebackground="red", variable=direction, value='CCW',
                            indicatoron='False', borderwidth=3, font='Helvetica 10')
    btnCCW.pack(side=TOP, padx=4, pady=4)
    ## Button functions
    def jog_function(action):
        Stage.jog(axisChoice.get(), jog_amount.get(), direction.get())
        update_table(axisChoice.get(), True)
    jog_button.bind("<Button-1>", jog_function)
    def go_to_position_function(action):
        Stage.goto_abs(axisChoice.get(), position_desired.get())
        update_table(axisChoice.get(), True)
    pos_button.bind("<Button-1>", go_to_position_function)

    # emergency stop  (WIP)
    xOct, yOct = 25, 25
    points = []
    for k in range(1,9):
        x0 = xOct * ( cos(2*k*pi / 8 + pi / 8) + 1 ) 
        y0 = yOct * ( sin(2*k*pi / 8 + pi / 8) + 1 )
        points.append(x0)
        points.append(y0)
    points = tuple(points)
    stop = Canvas(control_frame, bg='seashell2', width=50, height=50, highlightthickness=0, relief='raised')
    Stop = stop.create_polygon(points, smooth=False, fill='red', outline='black')
    stop.create_text(xOct, yOct, text='STOP!', fill="white", font=('Helvetica 10 bold'))
    stop.pack(fill = "both", side = RIGHT)
    def custom_stop(action):
        if int(Stage._verify_all_moving().strip().decode("utf-8")) != 0:
            Stage.slow_stop()
        stop.after(200, lambda: stop.itemconfig(Stop, fill="yellow"))
        stop.after(400, lambda: stop.itemconfig(Stop, fill="red"))
    stop.bind("<ButtonPress-1>", custom_stop)

    # Status table
    status_frame = LabelFrame(root, text=u'Stage Status', font='Helvetica 13', bg='light yellow')
    status_frame.pack(fill=BOTH)

    status_grid_frame = Frame(status_frame)
    status_grid_frame.pack(side=LEFT)
    cells = {}
    for row in range(7):
        for column in range(5):
            cell = Label(status_grid_frame, relief=RIDGE)
            cell.grid(row=row, column=column, sticky="ew")
            cells[(row, column)] = cell
    ## labels
    cells[(0,0)].configure(background='light gray')
    cells[(0,0)].configure(text='AXIS')
    for row in range(1,7):
        cells[(row, 0)].configure(text=[axis.name for axis in Axis][row-1])
    cells[(0,1)].configure(text='Driver Division', font='Helvetica 10')
    cells[(0,2)].configure(text='Resolution', font='Helvetica 10')
    cells[(0,3)].configure(text='Abs Position', font='Helvetica 10')
    cells[(0,4)].configure(text='Speed Set', font='Helvetica 10')
    ## table data
    def update_table(axis, all=False):
        while int(Stage._verify_all_moving().strip().decode("utf-8")) != 0:
            continue
        cells[(axis, 3)].configure(background='white')
        read_drvdiv = Stage._get_driver_division(axis)
        cells[(axis, 1)].configure(text=read_drvdiv, font='Helvetica 10', background='white')

        read_resolution = str(Stage._get_resolution(axis).strip().decode("utf-8"))
        cells[(axis, 2)].configure(text=read_resolution, font='Helvetica 10', background='white')
        i = 4
        read_speed = str(Stage._get_speed(axis).strip().decode("utf-8"))
        cells[(axis, i)].configure(text=read_speed, font='Helvetica 10', background='white')
        root.after(10, lambda: cells[(axis, i)].configure(background='spring green'))
        root.after(2000, lambda: cells[(axis, i)].configure(background='white'))
        if all:
            i = 3
            read_position = str(Stage._get_position(axis).strip().decode("utf-8"))
            cells[(axis, 3)].configure(text=read_position, font='Helvetica 10', background='white')
            root.after(10, lambda: cells[(axis, i)].configure(background='spring green'))
            root.after(2000, lambda: cells[(axis, i)].configure(background='white'))

    update_button = Button(status_frame, text=u'Update', font='Helvetica 12')
    update_button.pack(side=LEFT, padx=10)
    def full_table_refresh(action):
        update_button.configure(relief=SUNKEN, text='WAIT', bg='red', fg='white')
        root.update()
        for axis in Axis:
            update_table(axis.value, all=True)
        update_button.configure(relief=RAISED, text='Update', background='SystemButtonFace', fg='black')
    update_button.bind("<ButtonPress-1>", full_table_refresh)

    # copyright label
    copyright = Button(root, text=u'© 2021 Mabuchi Research Co. LTD.', relief=SUNKEN, font='Helvetica 8')
    copyright.pack(side=BOTTOM, fill=X)



    root.mainloop()