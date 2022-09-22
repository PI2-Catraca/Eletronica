import serial
import time
import adafruit_fingerprint

def verifica_digital(finger):
	"""Get a finger print image, template it, and see if it matches!"""
	print("Waiting for image...")
	while finger.get_image() != adafruit_fingerprint.OK: # adquire imagem da digital
	    pass
	print("Templating...")
	if finger.image_2_tz(1) != adafruit_fingerprint.OK: # gera template
	    return False
	print("Searching...")
	if finger.finger_search() != adafruit_fingerprint.OK: # busca template semelhante na memoria ROM
	    return False
	return True

def upload_template(finger, arquivo, posicao):
	print("Carregando arquivo de template...", end="", flush=True)
	with open(arquivo, "rb") as file:
	    data = file.read()
	finger.send_fpdata(list(data), "char", 1)

	i = finger.store_model(location=posicao,slot=1) # Cria o modelo com o template armazenado no buffer
											  # e armazena na posição 2 da memoria ROM do device
	if i == adafruit_fingerprint.OK:
	        print("Stored")
	else:
	    if i == adafruit_fingerprint.BADLOCATION:
	        print("Bad storage location")
	    elif i == adafruit_fingerprint.FLASHERR:
	        print("Flash storage error")
	    else:
	        print("Other error")
	    return False

def delete_template(finger, location):
	finger.delete_model(location)