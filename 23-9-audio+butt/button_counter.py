import time
import RPi.GPIO as GPIO

# Pins definitions
btn_pin = 4

# Set up pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(btn_pin, GPIO.IN)

# Our counter
counter = 0

# Remember the current and previous button states
current_state = True
prev_state = True

# If button is pushed, light up LED
try:
    while True:
        current_state = GPIO.input(btn_pin)
        if (current_state == False) and (prev_state == True):
            counter = counter + 1
            print(counter)
        prev_state = current_state

# When you press ctrl+c, this will be called
finally:
    GPIO.cleanup()