#!/usr/bin/python

import sys
import os
from LM76 import LM76
import RPi.GPIO as GPIO
import thread
from time import sleep

def main():
	SWITCH_PIN = 19
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(SWITCH_PIN,GPIO.IN)
	sensor = LM76(0x48)
	while True:
		input = GPIO.input(SWITCH_PIN)
		if (input==False):
			sleep(0.01)
			if (input==False):
				temp = sensor.getTemp()
				print "Temperature : " + `temp`
				int_temp = int(temp)
				if ((int_temp+0.5)<(temp-0.25)): 
					filename = "./lang/en/" + `int_temp+1` + ".0.wav"
				elif ((int_temp)>(temp-0.25)):
					filename = "./lang/en/" + `int_temp` + ".0.wav"
				else:
					filename = "./lang/en/" + `int_temp` + ".5.wav"
				command = "mplayer -framedrop " + filename + " ./lang/en/degree_celsius.wav >>/dev/null"
				os.system(command)
				sleep(0.5)

main()
