'''
http://wiki.seeedstudio.com/Grove-Ultrasonic_Ranger/
connections: 
Ground  - GND 
Power    - 3V3 
NC
Signal - pin Y9
'''

import utime
from machine import Pin

_TIMEOUT1 = 1000
_TIMEOUT2 = 1000
dio = Pin('X1')

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

def get_distance():
     while True:
          dist = _get_distance()
          if dist != None :
               if dist > 1:
                    return dist

print('Detecting distance...')
avg_dist = [0, 0, 0, 0, 0]


while True:
     x = get_distance()
     #print(x)
     for i in range(len(avg_dist)):
          avg_dist[i] = int(get_distance())
          print('avg_dist' , avg_dist)
          if i == 5:
               print('Done')
               y = sum(avg_dist)/len(avg_dist)
               print (y)
               if y < 30 :
                  print('Hug me')
                  utime.sleep(10)
               i = 0
     utime.sleep(1)







