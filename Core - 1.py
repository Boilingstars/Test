import RPi.GPIO as GPIO, cv2, atexit, websocket, json
from i2c_itg3205 import *
from i2c_adxl345 import *
from threading import Thread
from time import *

cars = []
yourCarPosition = []

def on_message(ws, mess):
    jmes = json.loads(mess)
    if jmes["action"] == "SendAllCoords":
        cars.append({carName:jmes["data"]["carName"], position: jmes["data"]["position"] })
    elif jmes["action"] == "SendPos":
        global yourCarPosition
        yourCarPosition = jmes["position"]

def on_close(ws):
    ws.close()

def on_open(ws):
    print("Connection open")

ws2 = websocket.WebSocketApp("ws://localhost:8765", on_message=on_message, on_close=on_close, on_open=on_open)
new_p2 = Thread(target=ws2.run_forever)
new_p2.start()
sleep(2)
itg3205 = i2c_itg3205(1)
adxl345 = i2c_adxl345(1)

# Set the type of GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Motor drive interface definition
ENA = 13  # //L298 Enable A
servo = 12  #
IN1 = 19  # //Motor interface 1
IN2 = 16  # //Motor interface 2
nul_ang = 38
nul = nul_ang/18 + 2

# Set the type of GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Motor initialized to LOW
GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(IN1, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(IN2, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(servo, GPIO.OUT)

pwmA = GPIO.PWM(ENA, 100)
pwmA.start(0)
# pwmServo.start(nul)

# Sensor distance
ECHO = 24
TRIG = 18
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(TRIG, GPIO.OUT, initial=GPIO.LOW)

cam = cv2.VideoCapture(2)

def close():
    print("end", flush=True)
    MotorStop()
    cam.release()
    cv2.destroyAllWindows()

def GetPosition():
    x = yourCarPosition[0]
    y = yourCarPosition[1]

    return x, y

def MotorForward(speed):
    print('motor forward')
    pwmA.ChangeDutyCycle(speed)
    GPIO.output(IN1, True)
    GPIO.output(IN2, False)


def MotorBackward(speed):
    print('motor backward')
    pwmA.ChangeDutyCycle(speed)
    GPIO.output(IN1, False)
    GPIO.output(IN2, True)


def MotorStop():
    print('motor stop')
    pwmA.ChangeDutyCycle(0)
    GPIO.output(IN1, True)  
    GPIO.output(IN2, True)

def set_angle(angle):
    print('angle', angle)
    pwmServo = GPIO.PWM(servo, 50)
    pwmServo.start(nul)
    duty = angle/18 + 2
    pwmServo.ChangeDutyCycle(duty)
    sleep(0.2)
    pwmServo.stop()

def GetImage():
    ret, image = cam.read()
    if ret:
        return ret, image
    else:
        return ret, False

