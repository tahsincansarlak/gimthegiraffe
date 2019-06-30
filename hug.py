import machine, network, ubinascii, ujson, urequests, utime
from pyb import Pin, Timer, UART
import utime, pyb, network, machine, gc

def hug():
    WAVE_TIME = 4
    ANGLE1 = -180
    ANGLE2 = 180
    steps1 = abs(ANGLE1)/WAVE_TIME
    steps2 = abs(ANGLE2)/WAVE_TIME

    servo1 = pyb.Servo(4) 
    servo2 = pyb.Servo(1)
    servo2.angle(0,1)
    servo1.angle(0,1)
    i = 1
    a1 = 1
    a2 = 1
    for i in range( WAVE_TIME+1):
        print('i is: ', i)
        servo1.angle(a1,1)
        servo2.angle(a2,1)
        utime.sleep(1)
        a1 = i*steps1
        a2 = i*steps2
        if(ANGLE1 < 0):
            a1 = a1*(-1)
        if(ANGLE2 < 0):
            a2 = a2*(-1)


def unhug():
    servo1 = pyb.Servo(4) 
    servo2 = pyb.Servo(1)
    servo2.angle(0,1)
    servo1.angle(0,1)

while(True):
    hug()
    print('Hi')






