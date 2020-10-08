#!/usr/bin/python
from time import sleep
import os
import sys
from Sensors import LM75
#from Sensors import PCF8563
import Adafruit_Nokia_LCD as LCD
import Adafruit_GPIO.SPI as SPI
import RPi.GPIO as GPIO
import Image
import ImageDraw
import ImageFont
import thread
import re
import datetime

#class Sensors(Thread):
#	def __init__(self):
#		Thread.__init__(self)
#	def run(self):
#		while True:
			
class TalkingHat():
	
	def __init__(self):
		self.LCD_DC = 5
		self.LCD_BL = 6
		self.LCD_RST = 22
		self.tempSensor = LM75(0x48)
		self.rtcSensor = 0 #incorporate rtc here
		self.time = '00:00:00'
		self.temp = '0'		

	def beginLCD(self):
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.LCD_BL,GPIO.OUT)
		GPIO.output(self.LCD_BL,GPIO.HIGH)
		self.Display = LCD.PCD8544(self.LCD_DC,self.LCD_RST, spi=SPI.SpiDev(0,0,max_speed_hz=4000000))
		self.Display.begin(contrast=60)
		self.Display.clear()
		self.Display.display()
	def clearImage(self):
		self.draw.rectangle((0,0,LCD.LCDWIDTH,LCD.LCDHEIGHT),outline=255,fill=255)
		self.Display.image(self.image)
		self.Display.display()

	def welcomeMessage(self):
		self.Display.clear()
		self.image =  Image.new('1',(LCD.LCDWIDTH,LCD.LCDHEIGHT))
		self.draw = ImageDraw.Draw(self.image)
		self.draw.rectangle((0,0,LCD.LCDWIDTH,LCD.LCDHEIGHT),outline=255, fill = 255)
		self.font = ImageFont.truetype('Lady Radical.ttf', 16)
		self.draw.text((6,2),'Welcome',font=self.font)
		self.draw.text((32,14),'to',font=self.font)
		self.draw.text((2,27),'Talking Hat',font=self.font)
		self.Display.image(self.image)
		self.Display.display() 
	def displayTime(self):
		self.draw.text((25,0),'Time',font=self.font)
                self.draw.text((20,20),self.time,font=self.font)
                #self.draw.text((15,30),'',font=self.font)
                self.Display.image(self.image)
                self.Display.display()

	def displayTemp(self):
		#self.font = ImageFont.load_default()
		self.temp=self.tempSensor.getTemp()
		self.draw.text((2,0),'Temperature',font=self.font)
		self.draw.text((35,15),`self.temp`,font=self.font)
		self.draw.text((15,30),'Celsius',font=self.font)
		self.Display.image(self.image)
		self.Display.display()						
		
def main():	
	GPIO.setwarnings(False)
	device = TalkingHat()
	device.beginLCD()
	device.welcomeMessage()
	sleep(1)
	while True:
		device.clearImage()
		device.displayTemp()
		sleep(0.1)
#	GPIO.cleanup()
main()	
