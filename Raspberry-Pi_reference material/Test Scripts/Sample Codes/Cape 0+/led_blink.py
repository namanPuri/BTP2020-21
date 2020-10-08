import RPi.GPIO as GPIO
from time import sleep

LED_PIN = 18

print "Setting up GPIO"
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN,GPIO.OUT)

def enable_led(should_enable):
	if should_enable:
		GPIO.output(LED_PIN,False)
	else:
		GPIO.output(LED_PIN, True)

while True:
	enable_led(False)
	sleep(0.5)
	enable_led(True)
	sleep(0.5)
GPIO.cleanup()
