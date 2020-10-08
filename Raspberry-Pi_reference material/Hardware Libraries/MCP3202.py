#!/usr/bin/python

import RPi.GPIO as GPIO
import spidev
from time import sleep

class MCP3202():
	CS = 0
	VDD = 3.3
	SPI = 0 
	def __init__(self,cspin,vdd=3.3):
		self.CS = cspin
		self.VDD = vdd
		self.SPI = spidev.SpiDev()
		self.SPI.open(0,self.CS)
		self.SPI.cshigh = False
		self.SPI.max_speed_hz = 122000
	def getVoltage(self,A):	
		B = (self.VDD*A)/4096
		return B
	def getReading(self,channel):
		code_word = 0x80&(channel<<6)
		reading = self.SPI.xfer([0x01, code_word, 0x00, 0x00, 0x00])
		#print reading
		readingMSB = ((reading[1]&0x0F)<<8)|reading[2]
		#print "MSBFirst: "+ `readingMSB`+ " and " + `self.getVoltage(readingMSB)`
		return readingMSB
	def getDiffReading(self,polarity):
		code_word = (polarity<<6)
                reading = self.SPI.xfer([0x01, code_word, 0x00, 0x00, 0x00])
                #print reading
                readingMSB = ((reading[1]&0x0F)<<8)|reading[2]
                #print "MSBFirst: "+ `readingMSB`+ " and " + `self.getVoltage(r$
		return readingMSB
#a = MCP3202(0,3.3)
#while True:
#	a.getReading(0)
#	sleep(0.1)
