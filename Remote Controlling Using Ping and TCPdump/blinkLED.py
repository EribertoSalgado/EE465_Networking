#!/usr/bin/env python3
import RPi.GPIO as GPIO
from time import sleep

# Set up the GPIO pin
LED_PIN = 17  # GPIO pin where the LED is connected

# Set up the GPIO mode
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

try:
    while True:
        GPIO.output(LED_PIN, GPIO.HIGH)  # Turn LED on
        sleep(1)                         # Wait 1 second
        GPIO.output(LED_PIN, GPIO.LOW)   # Turn LED off
        sleep(1)                         # Wait 1 second

except KeyboardInterrupt:
    # Clean up GPIO settings on exit
    pass
finally:
    GPIO.cleanup()
