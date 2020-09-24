import time
import RPi.GPIO as GPIO
import simpleaudio as sa

btn_pin = 4


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(btn_pin, GPIO.IN)


filename = 'applause-1.wav'
wave_obj = sa.WaveObject.from_wave_file(filename)


current_state = True
prev_state = False


try:
    while True:
        current_state = GPIO.input(btn_pin)
        if (current_state == False) and (prev_state == True):
            play_obj = wave_obj.play()
            play_obj.wait_done()

        prev_state = current_state

finally:
    GPIO.cleanup()

