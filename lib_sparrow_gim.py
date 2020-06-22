import RPi.GPIO as GPIO
from time import sleep
import paho.mqtt.client as mqtt
import sys
import json
global lib
#global lib_topic
broker_ip = 'localhost'
port = 1883

global lib_mqtt_client
lib={}

Tilt_Pin          = 12
Pan_Pin           = 16
SERVO_MAX_DUTY    = 12
SERVO_MIN_DUTY    = 3

GPIO.setmode(GPIO.BOARD)

GPIO.setup(Tilt_Pin, GPIO.OUT)
GPIO.setup(Pan_Pin, GPIO.OUT)

Tilt = GPIO.PWM(Tilt_Pin, 50)
Pan = GPIO.PWM(Pan_Pin, 50)
Tilt.start(0)
Pan.start(0)

def msw_mqtt_connect(broker_ip, port):
    lib_mqtt_client = mqtt.Client()
    lib_mqtt_client.on_connect = on_connect
    lib_mqtt_client.on_disconnect = on_disconnect
    lib_mqtt_client.on_subscribe = on_subscribe
    lib_mqtt_client.on_message = on_message
    lib_mqtt_client.connect(broker_ip, port)
    lib_muv_topic = '/MUV/control/'+ lib['name'] + '/MICRO'
    lib_mqtt_client.subscribe(lib_muv_topic, 0)
    print(lib_muv_topic)
    lib_mqtt_client.loop_start()
   # lib_mqtt_client.loop_forever()
    return lib_mqtt_client


def on_connect(client, userdata, flags, rc):
    print('[msg_mqtt_connect] connect to ', broker_ip)


def on_disconnect(client, userdata, flags, rc=0):
    print(str(rc))


def on_subscribe(client, userdata, mid, granted_qos):
    print("subscribed: " + str(mid) + " " + str(granted_qos))


def on_message(client, userdata, msg):
    payload = msg.payload.decode('utf-8')
    on_receive_from_msw(msg.topic, str(payload))


def request_to_mission(cinObj):
  con = cinObj['con']
  con_arr = con.split(',')
  
#  print(con)
#  tilt_value = cinObj['t']
#  pan_value = cinObj['p']
#  print(tilt_value)
#  print(pan_value)
  setServoTilt(con_arr[0])
  setServoPan(con_arr[1])


def on_receive_from_msw(topic, str_message):
    print('[' + topic + '] ' + str_message)
#    str_message = {"t":40,"p":90}
#    str_message = {"con":str_message}
#    print(str_message)
#    print(type(str_message))
#    cinObj = json.dumps(str_message)
    cinObj = json.loads(str_message)
    print(cinObj)
#    print(type(cinObj))
#    request_to_mission(str_message)
    request_to_mission(cinObj)
    
def setServoTilt(degree):
  if degree > 180:
    degree = 180

  duty = SERVO_MIN_DUTY+(degree*(SERVO_MAX_DUTY-SERVO_MIN_DUTY)/135.0)
  print("Tilt Degree: {} to {}(Duty)".format(degree, duty))

  Tilt.ChangeDutyCycle(duty)

def setServoPan(degree):
  if degree > 180:
    degree = 180
  
  duty = SERVO_MIN_DUTY+(degree*(SERVO_MAX_DUTY-SERVO_MIN_DUTY)/180.0)
  print("Pan Degree: {} to {}(Duty)".format(degree, duty))
  Pan.ChangeDutyCycle(duty)

def main ():
 try:
   global lib
   argv = sys.argv[1:]
   if argv != None:
     lib = {'name': argv[0]}
     print(lib)
     lib_mqtt_client = msw_mqtt_connect(broker_ip, port)
   else:
     print("Input the argv!")
 except KeyboardInterrupt:
   GPIO.cleanup()

if __name__ == "__main__":  
#  for i in range(40, 65, 5):
#    setServoTilt(i)
#    sleep(1)
#  for i in range(130 , 80, -5):
#    setServoPan(i)
#    sleep(1)
  main()
