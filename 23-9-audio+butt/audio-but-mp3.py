import time
import RPi.GPIO as GPIO
from pygame import mixer

# Pins definitions
btn_pin = 4

# Set up pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(btn_pin, GPIO.IN)

# Initialize pygame mixer
mixer.init()

# Remember the current and previous button states
current_state = True
prev_state = True

# Load the sounds
mixer.music.load('e:/LOCAL/Betrayer/Metalik Klinik1-Anak Sekolah.mp3')

# If button is pushed, light up LED
try:
    while True:
        current_state = GPIO.input(btn_pin)
        if (current_state == False) and (prev_state == True):
            mixer.music.play()
        prev_state = current_state

# When you press ctrl+c, this will be called
finally:
    GPIO.cleanup()
