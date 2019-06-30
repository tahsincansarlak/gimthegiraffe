import machine, network, ubinascii, ujson, urequests, utime
from pyb import Pin, Timer, UART
import utime, pyb, network, machine, gc

_TIMEOUT1 = 1000
_TIMEOUT2 = 10000
dio = Pin('X1')

#Moves the motors to give a hug.
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

#Moves the motors to the start position.
def unhug():
    servo1 = pyb.Servo(4) 
    servo2 = pyb.Servo(1)
    servo2.angle(0,1)
    servo1.angle(0,1)


#Uses the grove sensor to get distance. This part of the code is taken from Prof. Rogerss Github.
def _get_distance():
     dio.init(Pin.OUT)
     dio.value(0)
     utime.sleep_us(2)
     dio.value(1)
     utime.sleep_us(10)
     dio.value(0)

     dio.init(Pin.IN)

     t0 = utime.ticks_us()
     count = 0
     while count < _TIMEOUT1:
          if dio.value():
               break
          count += 1
          if count >= _TIMEOUT1:
               return None
     t1 = utime.ticks_us()
     count = 0
     while count < _TIMEOUT2:
          if not dio.value():
               break
          count += 1
          if count >= _TIMEOUT2:
               return None
     t2 = utime.ticks_us()
     dt = int(t1 - t0)
     if dt > 530:
          return None
     distance = ((t2 - t1) / 29 / 2)    # cm
     return distance


# Sends the distance if the distance is more than 1 and if there is a reading of distance.
def get_distance():
     while True:
          dist = _get_distance()
          if dist != None :
               if dist > 1:
                    return dist

# Creates an array to find the average of 5 last collected distances.
avg_dist = [0, 0, 0, 0, 0]

while True:
  x = get_distance()
  #Saves the last 5 distances in an array
  for i in range(len(avg_dist)):
    avg_dist[i] = int(get_distance())
    if i == 4:
    	#Takes the average of last 5 measures to have a more accurate distance reading.
      	y = sum(avg_dist)/(len(avg_dist)*10)
      		# If the distance is less than 30 cm, Gim will hug and then wait and unhug and wait until he starts reading the distance.
        	if y < 30 :
	        hug()
	        utime.sleep(2)
	        unhug()
	        utime.sleep(2)
	# Makes sure the new values are saved in the array.
    i = 0
  utime.sleep(1)


