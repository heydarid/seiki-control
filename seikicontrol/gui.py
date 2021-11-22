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

# main
if __name__ == '__main__':
    root = Tk()
    root.title(u'SURUGA-SEIKI STAGE CONTROL PROGRAM')
    root.geometry('1000x600')
    Stage = Seiki()

    # Axis selection
    axis_frame = Frame(root)
    axis_frame.pack(fill="x")
    axis_label = Label(axis_frame, text=u'Axis control:  ', font='Helvetica 15')
    axis_label.pack(side=LEFT)
    axisChoice = IntVar()
    for axis in Axis:
        btn = Radiobutton(axis_frame, text=axis.name, activebackground="red", variable=axisChoice, value=axis.value,
                            indicatoron='False', borderwidth=3, font='Helvetica 10')

        btn.pack(side=LEFT, padx=4, pady=4)

    # Speed selection
    speed_frame = Frame(root)
    speed_frame.pack(fill='x')
    speed_label = Label(speed_frame, text=u'Speed setting: ', font='Helvetica 15')
    speed_label.pack(side=LEFT)
    speedSet = IntVar()
    for speed in range(10):
        btnSpeed = Radiobutton(speed_frame, text=str(speed), activebackground="red", variable=speedSet, value=speed, 
                                indicatoron='False', borderwidth=3, font='Helvetica 10')
        btnSpeed.pack(side=LEFT, padx=4, pady=4)

    parent_left = Frame(root, bg='yellow')
    parent_left.pack(side=LEFT, expand=False, fill=BOTH)
    # Absolute position
    abs_pos_frame = Frame(parent_left)
    abs_pos_frame.pack(side=LEFT, expand=False, fill=BOTH)
    pos_label = Label(abs_pos_frame, text=u'POS', font='Helvetica 14')
    pos_label.pack(side=TOP)
    position_desired = Entry(abs_pos_frame, width=15)
    position_desired.pack()

    # Jogging with arrows (right is CW, left is CCW)
    jog_frame = Frame(parent_left)
    jog_frame.pack(side=LEFT, expand=False, fill=BOTH)
    jog_label = Label(jog_frame, text=u'JOG', font='Helvetica 14')
    jog_label.pack(side=TOP)

    direction = IntVar()
    btnCW = Radiobutton(jog_frame, text='CW', activebackground="red", variable=direction, value='CW',
                            indicatoron='False', borderwidth=3, font='Helvetica 10')
    btnCW.pack(side=TOP, padx=4, pady=4)
    jog_amount = Entry(jog_frame, width=15)
    jog_amount.pack(side=TOP)
    btnCCW = Radiobutton(jog_frame, text='CCW', activebackground="red", variable=direction, value='CCW',
                            indicatoron='False', borderwidth=3, font='Helvetica 10')
    btnCCW.pack(side=TOP, padx=4, pady=4)
    ### NEED A JOG BUTTON
    

    # Status table
    status_frame = Frame(root, bg = 'lime')
    status_frame.pack(side=LEFT, expand=False, fill=BOTH)

    status_label = Label(status_frame, text=u'STATUS', font='Helvetica 14', wraplength=1)
    status_label.pack(side=LEFT, fill='x')

    status_grid_frame = Frame(status_frame)
    status_grid_frame.pack(side=LEFT, fill='x')
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
    cells[(0,1)].configure(text='Drv Division')
    cells[(0,2)].configure(text='Resol')
    cells[(0,3)].configure(text='Abs Position')
    cells[(0,4)].configure(text='Speed Set')
    ## table data
    def update_table(axis):
        read_drvdiv = str(Stage._get_driver_division(axis).strip().decode("utf-8"))
        read_position = str(Stage._get_position(axis).strip().decode("utf-8"))
        read_resolution = str(Stage._get_resolution(axis).strip().decode("utf-8"))
        read_speed = str(Stage._get_speed(axis).strip().decode("utf-8"))
        cells[(axis, 1)].configure(text=read_drvdiv, background='white')
        cells[(axis, 2)].configure(text=read_resolution, background='white')
        cells[(axis, 3)].configure(text=read_position, background='white')
        cells[(axis, 4)].configure(text=read_speed, background='white')
        [root.after(10, lambda: cells[(axis, i)].configure(background='red')) for i in range(1,5)]
        [root.after(2000, lambda: cells[(axis, i)].configure(background='white')) for i in range(1,5)]
    # [update_table(axis.value) for axis in Axis]  # Initialize
    

    # Execute action
    exec_frame = Frame(root, borderwidth=4)
    exec_frame.pack(padx=10, pady=10)
    def options():
        Stage.set_speed(axisChoice.get(), speedSet.get())
        update_table(axisChoice.get())
        Stage.goto_abs(axisChoice.get(), position_desired.get())
        update_table(axisChoice.get())
    execButton = Button(exec_frame, text="GO & REFRESH",  font='Helvetica 10', width=15, height=2, command=options)
    execButton.pack()

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
    stop = Canvas(root, width=50, height=50, highlightthickness=0, relief='raised')
    Stop = stop.create_polygon(points, smooth=False, fill='red', outline='black')
    stop.create_text(xOct, yOct, text='STOP!', fill="white", font=('Helvetica 10 bold'))
    stop.place(anchor='se', relx=1.0, rely=1.0)
    def custom_stop(action):
        if int(Stage._verify_all_moving().strip().decode("utf-8")) != 0:
            Stage.slow_stop()
        stop.itemconfig(Stop, fill='yellow')
        stop.itemconfig(Stop, fill='purple')

    stop.bind("<ButtonPress-1>", custom_stop)

    root.mainloop()