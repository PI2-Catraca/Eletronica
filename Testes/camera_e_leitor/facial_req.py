#!/usr/lib/python3.9

# import the necessary packages
import I2C_LCD_driver
from imutils.video import VideoStream
from imutils.video import FPS
import face_recognition
import imutils
import pickle
import serial
import time
import adafruit_fingerprint
import cv2
import signal
from leitor_biometrico import verifica_digital, upload_template
from sensor_de_distancia import distance
import RPi.GPIO as GPIO
from motor import abre_portao, fecha_portao
from ultimoArquivo import ultimoArquivoModificado

class TimeOutException(Exception):
   pass
 
def alarm_handler(signum, frame):
    print("ALARM signal received")
    raise TimeOutException()
signal.signal(signal.SIGALRM, alarm_handler) 

def presenca_usuario():
    distancia = distance(GPIO_TRIGGER_DISTANCIA,GPIO_ECHO_DISTANCIA)
    print(f'Distancia = {distancia}')
    tempo_transcorrido = 0
    inicio = time.time()
    while (tempo_transcorrido < 5):
        print(f'Tempo transcorrido = {tempo_transcorrido}')
        while(distancia <= 98):
            inicio = time.time()
            distancia = distance(GPIO_TRIGGER_DISTANCIA,GPIO_ECHO_DISTANCIA)
            print(f'Distancia = {distancia}')
            time.sleep(1)
        tempo_transcorrido = time.time() - inicio

#-------------Setup dos pinos de saida e entrada------------#
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

#set GPIO Pins
GPIO_TRIGGER_PRESENCA = 10
GPIO_ECHO_PRENSENCA = 9

GPIO_TRIGGER_DISTANCIA = 17
GPIO_ECHO_DISTANCIA = 27

GPIO_MOTOR_R = 26
GPIO_MOTOR_L = 19

GPIO_ENCODER = 13


GPIO.setup(GPIO_ECHO_PRENSENCA, GPIO.IN)
GPIO.setup(GPIO_TRIGGER_PRESENCA, GPIO.OUT)

GPIO.setup(GPIO_ECHO_DISTANCIA, GPIO.IN)
GPIO.setup(GPIO_TRIGGER_DISTANCIA, GPIO.OUT)

GPIO.setup(GPIO_MOTOR_R, GPIO.OUT)
GPIO.setup(GPIO_MOTOR_L, GPIO.OUT)

GPIO.setup(GPIO_ENCODER, GPIO.IN)
GPIO.add_event_detect(GPIO_ENCODER, GPIO.BOTH)


#--------- Inicializando display LCD --------------#
lcdi2c = I2C_LCD_driver.lcd()
lcdi2c.lcd_clear()
lcdi2c.lcd_display_string("Iniciando", 1,0)
lcdi2c.lcd_display_string("Sistema", 2,0)
time.sleep(4)
lcdi2c.lcd_clear()


#- Configurando UART para comunicacao com o leitor biometrico -#
uart = serial.Serial("/dev/ttyUSB0", baudrate=57600, timeout=1)
finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)

#Initialize 'currentname' to trigger only when a new person is identified.
currentname = "unknown"
#Determine faces from encodings.pickle file model created from train_model.py
encodingsP = "encodings.pickle"

# initialize the video stream and allow the camera sensor to warm up
# Set the ser to the followng
# src = 0 : for the build in single web cam, could be your laptop webcam
# src = 2 : I had to set it to 2 inorder to use the USB webcam attached to my laptop
#vs = VideoStream(src=2,framerate=10).start()# src=2 originally
vs = VideoStream(usePiCamera=True).start()
time.sleep(1.0)

# start the FPS counter
fps = FPS().start()
arquivo_dat = ''

while True:
    teste = 0
    verif_digital = False
    lcdi2c.lcd_display_string("Data: %s" %time.strftime("%d/%m/%y"), 1,1)
    lcdi2c.lcd_display_string("Hora: %s" %time.strftime("%H:%M:%S"), 2,1)
    presenca = distance(GPIO_TRIGGER_PRESENCA,GPIO_ECHO_PRENSENCA)
    print(presenca)
    time.sleep(1.0)   
    while(presenca <= 60.0):
        lcdi2c.lcd_clear()
        lcdi2c.lcd_display_string("Processando...", 1,0)

        # Atualizando arquivos da digital
        if (arquivo_dat != ultimoArquivo()[0]):
            arquivo_dat = ultimoArquivo()[0]
            posicao_finger = ultimoArquivo()[1]
            upload_template(finger, arquivo_dat, posicao_finger)
            
        # load the known faces and embeddings along with OpenCV's Haar
        # cascade for face detection
        # print("[INFO] loading encodings + face detector...")
        data = pickle.loads(open(encodingsP, "rb").read())
        # grab the frame from the threaded video stream and resize it
        # to 500px (to speedup processing)
        frame = vs.read()
        frame = imutils.resize(frame, width=500)
        # Detect the fce boxes
        boxes = face_recognition.face_locations(frame)
        # compute the facial embeddings for each face bounding box
        encodings = face_recognition.face_encodings(frame, boxes)
        names = []
        
        # loop over the facial embeddings
        for encoding in encodings:
            # attempt to match each face in the input image to our known
            # encodings
            matches = face_recognition.compare_faces(data["encodings"],
                encoding)
            name = "Unknown" #if face is not recognized, then print Unknown
            
            # check to see if we have found a match
            if True in matches:
                teste = 0
                # find the indexes of all matched faces then initialize a
                # dictionary to count the total number of times each face
                # was matched
                matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                counts = {}

                # loop over the matched indexes and maintain a count for
                # each recognized face face
                for i in matchedIdxs:
                    name = data["names"][i]
                    counts[name] = counts.get(name, 0) + 1

                # determine the recognized face with the largest number
                # of votes (note: in the event of an unlikely tie Python
                # will select first entry in the dictionary)
                name = max(counts, key=counts.get)

                #If someone in your dataset is identified, print their name on the screen
                if currentname != name:
                    currentname = name
                    print(currentname)
                
                lcdi2c.lcd_clear()
                lcdi2c.lcd_display_string("Acesso", 1,5)
                lcdi2c.lcd_display_string("Liberado", 2,4)

                presenca_usuario()
                
            else:
                teste = teste + 1
                print(teste)
                lcdi2c.lcd_clear()
                lcdi2c.lcd_display_string("Tentativa de", 1,2)
                lcdi2c.lcd_display_string(f"reconhecimento {teste}", 2,0)
                if teste == 3:
                    signal.alarm(30)
                    try:
                        lcdi2c.lcd_clear()
                        lcdi2c.lcd_display_string("Coloque sua", 1,0)
                        lcdi2c.lcd_display_string("digital", 2,0)
                        verif_digital = verifica_digital(finger)
                    except TimeOutException as ex:
                        print(ex)            
                    signal.alarm(0)
                    teste = 0
                    if verif_digital:
                        lcdi2c.lcd_clear()
                        lcdi2c.lcd_display_string("Acesso", 1,5)
                        lcdi2c.lcd_display_string("Liberado", 2,4)
                        presenca_usuario()   
                    else:
                        lcdi2c.lcd_clear()
                        lcdi2c.lcd_display_string("Acesso", 1,5)
                        lcdi2c.lcd_display_string("Negado", 2,5)
                        


            # update the list of names
            names.append(name)


        # display the image to our screen
        cv2.imshow("Facial Recognition is Running", frame)
        key = cv2.waitKey(1) & 0xFF

        # quit when 'q' key is pressed
#         if key == ord("q"):
#             break

        # update the FPS counter
        fps.update()
        
        presenca = distance(GPIO_TRIGGER_PRESENCA,GPIO_ECHO_PRENSENCA)
        print(presenca)
        time.sleep(1.0)

# stop the timer and display FPS information
fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()
