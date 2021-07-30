"""
Project Name    : Python sample program
File Name       : control
Creation Date   : June-13-2019

Copyright 2019 SURUGA SEIKI Co.,Ltd. All rights reserved.
"""


import serial
import serial.tools.list_ports
import tkinter


# search com port
def search_com_port():
    com_s = serial.tools.list_ports.comports()
    com_list = []
    for com in com_s:
        com_list.append(com.device)

    if len(com_list) == 0:
        print("port invalid")
        return 'COM'
    else:
        use_port = com_list[0]
        print('enable port: ' + use_port)
        return use_port


# send and receive
def serial_write_read(ser, write_data, read_size):
    # Write
    ser.write(write_data)
    print('Send: ' + str(write_data))

    # Read
    read_data = ser.read_until(size=read_size)
    print('Recv: ' + str(read_data))

    return read_data


# send button click
def send_button_click(event):
    # Init Serial Port Setting
    ser = serial.Serial('COM' + txtCom.get(), txtBaudrate.get(), timeout=0.5)

    val = txtSend.get()
    w_data = (val + '\r').encode('utf-8')
    r_size = 256
    r_data = serial_write_read(ser, w_data, r_size)
    lblRecv.delete(0, tkinter.END)
    lblRecv.insert(tkinter.END, r_data)


# main
if __name__ == '__main__':

    # Window
    root = tkinter.Tk()
    root.title(u"Python sample program for DS102/112 Controller")
    root.geometry("450x300")

    # Send data
    lblSend = tkinter.Label(text=u'Send data')
    lblSend.place(x=50, y=30)

    txtSend = tkinter.Entry(width=50)
    txtSend.insert(tkinter.END, "AXI1:GOABS 100")
    txtSend.place(x=50, y=50)

    value = txtSend.get()

    btnSend = tkinter.Button(text=u'Send')
    btnSend.bind("<Button-1>", send_button_click)
    btnSend.place(x=360, y=50)

    # Receive data
    lblReceive = tkinter.Label(text=u'Receive data')
    lblReceive.place(x=50, y=100)

    lblRecv = tkinter.Entry(width=50)
    lblRecv.place(x=50, y=120)

    # Parameter
    lblParam = tkinter.Label(text=u'Parameter for serial communication')
    lblParam.place(x=50, y=170)

    # Com
    lblCom = tkinter.Label(text=u'COM Number :')
    lblCom.place(x=50, y=200)

    txtCom = tkinter.Entry(width=20)
    txtCom.place(x=160, y=200)

    # Baudrate
    lblBaudrate = tkinter.Label(text=u'Baudrate :')
    lblBaudrate.place(x=50, y=230)

    txtBaudrate = tkinter.Entry(width=20)
    txtBaudrate.insert(tkinter.END, "38400")
    txtBaudrate.place(x=160, y=230)

    # search com port
    port = search_com_port()
    no = port.replace("COM", "")
    txtCom.insert(tkinter.END, no)

    root.mainloop()
