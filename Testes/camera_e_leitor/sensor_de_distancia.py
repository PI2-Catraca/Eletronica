import RPi.GPIO as gp
import time


def distance(GPIO_TRIGGER, GPIO_ECHO):
  gp.output(GPIO_TRIGGER,gp.HIGH)
  time.sleep(0.00001)
  gp.output(GPIO_TRIGGER,gp.LOW)
  
  
  while (gp.input(GPIO_ECHO) == 0):
     inicio = time.time()

  while (gp.input(GPIO_ECHO) == 1):
     tempo_parado = time.time()
  
  
  if (gp.input(GPIO_ECHO) == 0):
    tempo_transcorrido = tempo_parado - inicio
    distancia = (tempo_transcorrido*34300)/2
    return distancia
  else:
    return 0
