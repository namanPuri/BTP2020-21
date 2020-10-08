import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setup(23,GPIO.IN)
while True:
	input_state = GPIO.input(23)
	print input_state

