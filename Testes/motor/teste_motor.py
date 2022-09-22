from motor import SetAngle, abre_portao, fecha_portao
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

GPIO_MOTOR_R = 26
GPIO_MOTOR_L = 19

GPIO_ENCODER = 13


GPIO.setup(GPIO_MOTOR_R, GPIO.OUT)
GPIO.setup(GPIO_MOTOR_L, GPIO.OUT)

GPIO.setup(GPIO_ENCODER, GPIO.IN)
GPIO.add_event_detect(GPIO_ENCODER, GPIO.BOTH)

while True:
    R_L = int(input())
    #passos = int(input())
    
    if(R_L == 1): # Anti-horário
        fecha_portao(GPIO_MOTOR_R, GPIO_ENCODER)
    elif(R_L == 2): # Horário
        abre_portao(GPIO_MOTOR_L, GPIO_ENCODER)
        