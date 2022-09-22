from sensor_de_distancia import distance
import RPi.gpio as GPIO

GPIO.setmode(GPIO.BCM)

GPIO_TRIGGER_PRESENCA = 10
GPIO_ECHO_PRENSENCA = 9

GPIO.setup(GPIO_ECHO_PRENSENCA, GPIO.IN)
GPIO.setup(GPIO_TRIGGER_PRESENCA, GPIO.OUT)

n_amostras = 100
amostra = 1
file =  open('sensor_presenca_cm.txt','w')

while amostra <= 100:
    distancia = distance(GPIO_TRIGGER_PRESENCA, GPIO_ECHO_PRENSENCA)
    file.write(f'{distancia}\n')
    amostra = amostra + 1

