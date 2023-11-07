#!/usr/bin/python


import time
from multiprocessing import Process
import serial

class Control:
    def __init__(self, queue, comPort, baudRate, verbose="False"):
        self.q = queue
        self.verbose = verbose
        self.speed = 0
        self.direction = 0

        self.comPort = comPort
        self.baudRate = baudRate
        self.ser = None

    def start(self):
        self.p = Process(target=self.run, args=(self.q))
        self.p.start()

    def connect(self):
        try:
            ser = serial.Serial(self.comPort, self.baudRate)
            self.ser = ser

        except serial.SerialException:
            print("Serial port not found, using dev mode by printing output!")
            self.ser = None

    def sendToArduino(self, sendStr, ser):
        ser.write(sendStr.encode('utf-8'))

    def sign(value):
        if value < 0:
            return -1
        if value == 0:
            return 0
        if value > 0:
            return 1

    def run(self):
        inp = (0, 0, 0)
        self.connect()
        while True:
            try:
                inp = self.q.get_nowait()
                print("TRY WORKED")
            except:
                time.sleep(0.000001)
                pass

            if True:        
                if inp[0] == "left": # left stick
                    axis = inp[1] #x
                    self.direction = self.sign(axis)
                    self.speed = abs(float(axis))
                    print(inp)

                if self.ser == None:
                    pass
                    #print(inp)
