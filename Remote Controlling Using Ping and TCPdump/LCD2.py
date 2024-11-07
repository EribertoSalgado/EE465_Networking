#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time
import netifaces as ni
from RPLCD.gpio import CharLCD

#Set the Mode for the pins
GPIO.setmode(GPIO.BCM)

GPIO.setup(7,GPIO.OUT)
GPIO.setup(8,GPIO.OUT)
GPIO.setup(26,GPIO.OUT)
GPIO.setup(19,GPIO.OUT)
GPIO.setup(13,GPIO.OUT)
GPIO.setup(6,GPIO.OUT)
GPIO.setup(27,GPIO.OUT)
GPIO.setup(22,GPIO.OUT)

lcd = CharLCD(pin_rs=7,pin_e=8,pins_data=[25,24,23,18],
        numbering_mode=GPIO.BCM,
        cols=20, rows=1,
        auto_linebreaks=False)
ni.ifaddresses('wlan0')
ip = ni.ifaddresses('wlan0')[ni.AF_INET][0]['addr']

try:
        while True:
                lcd.clear()
                lcd.cursor_pos = (0,0)
                lcd.write_string(ip)
                time.sleep(2)
                ni.ifaddresses('wlan0')
                ip = ni.ifaddresses('wlan0')[ni.AF_INET][0]['addr']
except KeyboardInterrupt:
        lcd.clear()
        GPIO.cleanup()
