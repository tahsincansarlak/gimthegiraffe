import machine, network, ubinascii, ujson, urequests, utime
from pyb import Pin, Timer

def connect_wifi():
     WiFi = network.WLAN()

     mac = ubinascii.hexlify(network.WLAN().config("mac"),":").decode()
     print("MAC address: " + mac)
     def connect():
          if not WiFi.isconnected():
               print ("Connecting ..")
               WiFi.active(True)
               WiFi.connect("Tufts_Wireless","")
               i=0
               while i < 25 and not WiFi.isconnected():
                    utime.sleep_ms(200)
                    i=i+1
               if WiFi.isconnected():
                    print ("Connection succeeded")
               else:
                    print ("Connection failed")     

     connect()
     print ("WiFi: ",WiFi.isconnected())

def systemlink_info_get_right():
     # Info
     Tag = "motor1"
     Type = "DOUBLE"
     Key = "lsf4DcHBczXKtrMjfW6JdAAbyU_8wxfbo9XkcWwKjW"

     urlBase = "https://api.systemlinkcloud.com/nitag/v2/tags/"
     urlTag = urlBase + Tag
     urlValue = urlBase + Tag + "/values/current"
     headers = {"Accept":"application/json","x-ni-api-key":Key}

     ## GET
     response = urequests.get(urlValue,headers=headers)
     value = response.text
     response.close()
     data = ujson.loads(value)
     result = data.get("value").get("value")
     #print ("value = ",result)
     result = float(result)
     return result

def systemlink_info_get_left():
     # Info
     Tag = "motor2"
     Type = "DOUBLE"
     Key = "lsf4DcHBczXKtrMjfW6JdAAbyU_8wxfbo9XkcWwKjW"

     urlBase = "https://api.systemlinkcloud.com/nitag/v2/tags/"
     urlTag = urlBase + Tag
     urlValue = urlBase + Tag + "/values/current"
     headers = {"Accept":"application/json","x-ni-api-key":Key}

     ## GET
     response = urequests.get(urlValue,headers=headers)
     value = response.text
     response.close()
     data = ujson.loads(value)
     result = data.get("value").get("value")
     #print ("value = ",result)
     result = float(result)
     return result

def move_motor1(right,left):

     #W16 has Timer2, Channel1
     Apwm=Pin('W16')
     timerA=Timer(2, freq=1000)
     chA=timerA.channel(1, Timer.PWM, pin=Apwm)

     Ain1=Pin('W22', Pin.OUT_PP)
     Ain2=Pin('W24', Pin.OUT_PP)

     standBy=Pin('W29', Pin.OUT_PP)

     #W29 has Timer1, Channel3
     Bpwm=Pin('Y12')
     timerB=Timer(1, freq=1000)
     chB=timerB.channel(3, Timer.PWM, pin=Bpwm)

     Bin1=Pin('W30', Pin.OUT_PP)
     Bin2=Pin('W32', Pin.OUT_PP)

     def clockwise(motor, speed):
          if motor=='a':
               Ain1.high()
               Ain2.low()
               chA.pulse_width_percent(speed)
          elif motor=='b':
               Bin1.high()
               Bin2.low()
               chB.pulse_width_percent(100-speed)
     def stop(motor):
          if motor=='a':
               Ain1.low()
               Ain2.low()
               chA.pulse_width_percent(0)
          elif motor=='b':
               Bin1.low()
               Bin2.low()
               chB.pulse_width_percent(0)


     def main():
          standBy.high()
          while(True):
               stop('a')
               stop('b')
               clockwise('a',50)
               clockwise('b',50)
               utime.sleep_ms(2500)
               break
               utime.sleep(1)
     main()

connect_wifi()

while (True):
     systemlink_info_get_right()
     systemlink_info_get_left()
     speed_right = systemlink_info_get_right()
     speed_left = systemlink_info_get_left()
     move_motor1(speed_right,speed_left)
