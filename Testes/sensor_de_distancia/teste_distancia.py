from sensor_de_distancia import distance
import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)

GPIO_TRIGGER_DISTANCIA = 17
GPIO_ECHO_DISTANCIA = 27

GPIO.setup(GPIO_ECHO_DISTANCIA, GPIO.IN)
GPIO.setup(GPIO_TRIGGER_DISTANCIA, GPIO.OUT)

n_amostras = 100
amostra = 1
file =  open('sensor_distancia_80cm.txt','w')

while amostra <= 100:
    distancia = distance(GPIO_TRIGGER_DISTANCIA, GPIO_ECHO_DISTANCIA)
    print(f'Distância = {distancia}')
    sleep(1)
    file.write(f'{distancia}\n')
    amostra = amostra + 1


