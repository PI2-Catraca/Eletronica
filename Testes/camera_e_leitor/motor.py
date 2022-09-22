import RPi.GPIO as GPIO

def SetAngle(passos, GPIO_MOTOR, GPIO_ENCODER):
    pwm = GPIO.PWM(GPIO_MOTOR, 1000)
    pwm.start(10)
    pos = 0
    while(pos < passos):
        if (GPIO.event_detected(GPIO_ENCODER)):
            pos = pos + 1
        print(f'POSIÇÃO = {pos}')
    pwm.stop()
    
def abre_portao(GPIO_MOTOR, GPIO_ENCODER):
    SetAngle(7, GPIO_MOTOR, GPIO_ENCODER)

def fecha_portao(GPIO_MOTOR, GPIO_ENCODER):
    SetAngle(7, GPIO_MOTOR, GPIO_ENCODER)
