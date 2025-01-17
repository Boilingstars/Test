import RPi.GPIO as GPIO
import cv2
from time import *
import atexit
from i2c_itg3205 import *
from i2c_adxl345 import *
import websocket
import json
from threading import Thread

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

cam = cv2.VideoCapture(0)

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

def GetDistance():
    '''
      Determine the distance to the nearest obstacle in centimeters. Return distance and error.
      If everything is OK: distance, "OK"
      If the response waiting time is exceeded: 0, "Timeout"
      If the distance exceeds 3 meters or is equal to 0: distance, "Out of reach"
   '''

    StartTime = time()
    StopTime = time()
    GPIO.output(TRIG, False)
    sleep(0.1)
    GPIO.output(TRIG, True)
    sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO) == 0:
        StartTime = time()

    while GPIO.input(ECHO) == 1:
        StopTime = time()

    pulseDuration = (StopTime - StartTime)
    distance = pulseDuration * 17000
    if pulseDuration >= 0.01746:
        return 0, 'Time out'
    elif distance > 300 or distance == 0:
        return distance, 'Out of range'

    return distance, 'Ok'

data = GetPosition()
if data:
    x = data[0]
    y = data[1]
    print("x = ", x, flush=True)
    print("y = ", y, flush=True)
else:
    print("none position!", flush=True)

def GetImage():
    '''
      Return picture from video camera
   '''
    ret, image = cam.read()
    if ret:
        return ret, image
    else:
        return ret, False

# Разбиваем карту на примерные ключевые точки
x_A = 4.73
y_B = 0.38
x_C = 0.42
y_D = 1.6
x_E = 1.76

points = [x_A, y_B, x_C, y_D, x_E]
signs = ["+", "-", "-", "+", "+"]

# Функция для проверки достижения точки 
def is_at_point(current_position, target_position, coordinate, sgn):
    x, y = current_position

    if coordinate == 1:
        t = x

    elif coordinate == 2:
        t = y
    
    if sgn == "+":
        if t <= target_position + 0.005:
            return True
        else:
            return False
        
    elif sgn == "-":
        if t <= target_position - 0.005:
            return True
        else:
            return False

# Функция для движения машины из точки A в точку B
def drive_to_point_A_to_B(next_point, coordinate, sgn):

    global queue
    position = GetPosition()

    # Начинаем прямолинейное движение...
    MotorForward(45)

    # ...пока машина не достигла точки поворота
    while not is_at_point(position, next_point, coordinate, sgn):
        # Получить текущее местоположение
        position = GetPosition()

    # Как только точка поворота достигнута
    MotorStop()
    sleep(1)
    # Останавливаем машину и разворачиваемся на 90 градусов вправо
    set_angle(72)
    MotorForward(45)
    sleep(0.8)
    MotorStop()
    sleep(0.8)
    set_angle(nul)
    sleep(0.8)

    # Меняем порядок координат
    if coordinate == 1:
        coordinate = 2
    elif coordinate == 2:
        coordinate = 1

    # Переходим к следующей точке
    queue += 1

    # Перевызываем функцию движения для следующей точки
    drive_to_point_A_to_B(points[queue], coordinate, signs[queue])

# Запуск движения
queue = 0
drive_to_point_A_to_B(points[queue], 1, signs[queue])