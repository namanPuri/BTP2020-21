#!/usr/bin/python

import time
import os
import RPi.GPIO as GPIO

class MCP3202():
	cspin = 8	
	mosi = 10
	miso = 9
	clk = 11
	def getReading(self,adcnum):
		if adcnum>1 or adcnum<0 :
			return -1;
		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)
		GPIO.setup(self.cspin, GPIO.OUT)
		GPIO.setup(self.mosi, GPIO.OUT)
		GPIO.setup(self.miso, GPIO.IN)
		GPIO.setup(self.clk, GPIO.OUT)

		GPIO.output(self.cspin, True)
		GPIO.output(self.clk,True)
		GPIO.output(self.cspin, False)
		commandout = adcnum << 1
		commandout |= 0x0D
		commandout <<= 4

		for i in range(4):
			if commandout & 0x80 :
				GPIO.output(self.mosi, True)		
			else:
				GPIO.output(self.mosi, False)
			commandout <<=1
			GPIO.output(self.clk,True)
			GPIO.output(self.clk,False)
		adcout = 0
		for i in range(13):
			GPIO.output(self.clk, True)
			GPIO.output(self.clk,False)
			adcout<<=1
			if GPIO.input(self.miso):
				adcout |=0x01
		GPIO.output(self.cspin, True)
		adcout /= 2
		return adcout 

A = MCP3202()
try:
	while True:
		b =A.getReading(0)
		print b
except KeyboardInterrupt :
	exit()
