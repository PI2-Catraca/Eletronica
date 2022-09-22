import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)

GPIO_TRAVA = 18

GPIO.setup(GPIO_TRAVA, GPIO.OUT)

while True:
    GPIO.output(GPIO_TRAVA, GPIO.LOW)
    sleep(1)
    GPIO.output(GPIO_TRAVA, GPIO.HIGH)
    sleep(1)


    
