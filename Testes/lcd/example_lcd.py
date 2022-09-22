#Programa: Display LCD I2C com Raspberry Pi
#Autor: Arduino e Cia

import I2C_LCD_driver
import socket
import fcntl
import struct
import time

lcdi2c = I2C_LCD_driver.lcd()

#Exibe informacoes iniciais
lcdi2c.lcd_display_string("Arduino e Cia", 1,1)
lcdi2c.lcd_display_string("LCD I2C e RPi", 2,1)
time.sleep(4)

#Apaga o display
lcdi2c.lcd_clear()

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915, 
        struct.pack('256s', ifname[:15])
    )[20:24])

#Mostra o endereco IP
#lcdi2c.lcd_display_string("IP", 1)
#lcdi2c.lcd_display_string(get_ip_address('wlan0'), 1,3)
 
while True:
#Mostra a data no display
    teste = 2
    lcdi2c.lcd_display_string("Tentativa de", 1,2)
    lcdi2c.lcd_display_string(f"reconhecimento {teste}", 2,0)