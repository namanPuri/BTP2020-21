#!/usr/bin/python
from time import sleep
import os
import sys
from Sensors import LM75
from Sensors import PCF8563
import Adafruit_Nokia_LCD as LCD
import Adafruit_GPIO.SPI as SPI
import RPi.GPIO as GPIO
import Image
import ImageDraw
import ImageFont
import thread
import re
import datetime
import netifaces as ni
import socket

class TalkingHat():
	def __init__(self):
		self.LCD_DC = 5
		self.LCD_BL = 6
		self.LCD_RST = 22
		
		self.tempSensor = LM75(0x48)
		self.rtcSensor = PCF8563(1,0x51) 
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
		self.font8 = ImageFont.truetype('Lady Radical.ttf',8)
		self.draw.text((6,2),'Welcome',font=self.font)
		self.draw.text((32,14),'to',font=self.font)
		self.draw.text((2,27),'Talking Hat',font=self.font)
		self.Display.image(self.image)
		self.Display.display() 

	def displayTime(self):
		self.draw.text((25,0),'Time',font=self.font)
	        #self.time = datetime.datetime.now().strftime("%H:%M:%S")
        	self.time = '{:2d}'.format(self.rtcSensor._read_hours()) +":"+ '{:2d}'.format(self.rtcSensor._read_minutes())+":"+ '{:2d}'.format(self.rtcSensor._read_seconds())
        	self.draw.text((20,20),self.time,font=self.font)
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
		return self.temp	

	def displayBye(self):
		self.draw.text((25,0),'Bye-Bye',font=self.font)
		self.Display.image(self.image)
		self.Display.display()

	def displayIPHost(self):
		self.default_font = ImageFont.truetype('NDS12.ttf', 8)
		self.draw.text((0,0),'Hostname: ',font=self.default_font)
		self.draw.text((5,8),socket.gethostname(),font = self.default_font)	
		self.draw.text((0,16),'Ethernet: ',font=self.default_font)
		try:
			self.draw.text((5,24),ni.ifaddresses('eth0')[2][0]['addr'],font= self.default_font)			
		except:
			self.draw.text((5,24), 'NC', font= self.default_font)
		self.draw.text((5,32),'WiFi: ',font=self.default_font)
		try:
			self.draw.text((5,40),ni.ifaddresses('wlan0')[2][0]['addr'],font = self.default_font)
		except:
			self.draw.text((5,40),'NC',font=self.default_font)		
		self.Display.image(self.image)
		self.Display.display()
def main():	
	#Preparing the GPIO
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(4, GPIO.OUT)
	GPIO.output(4,GPIO.LOW)
	
	LANG = 17
	SPEAK = 26
	time = 0
	temp = 0
	READY = 4
	langIndex = 0
	langList = [ ]
	lang = 0
	displayFlag = 0
	mode = 0
	
	GPIO.setup(LANG,GPIO.IN)
	GPIO.setup(SPEAK,GPIO.IN)
	langList = os.listdir('./lang/support')
	for index in range(len(langList)):
		langList[index] = langList[index][:-4]
	lang=langList[0]
	langIndex = 0
	mode =0 
	if (GPIO.input(SPEAK)==False):
		mode=1
	device = TalkingHat()
	device.beginLCD()
	device.welcomeMessage()
	sleep(1)
	if (mode == 1):
		device.clearImage()
		device.displayIPHost()
		while(GPIO.input(SPEAK)==False):
			device.displayIPHost()
			mode = 0
	GPIO.output(READY,GPIO.HIGH)	
	device.clearImage()
	device.displayTime()
	while True:
		device.clearImage()
		device.displayTime()
		if (GPIO.input(LANG) == False):
			sleep(0.01)
			if (GPIO.input(LANG)==False):
				langIndex = langIndex + 1
				if langIndex >= len(langList):
					langIndex = 0 					
				lang = langList[langIndex]
				command = "mplayer ./lang/support/" + langList[langIndex] + ".wav >>/dev/null"
                               	os.system(command)
		if (GPIO.input(SPEAK) == False):
                	sleep(0.01)
                	if (GPIO.input(SPEAK)==False):
				displayFlag = 1
				device.clearImage()
				temp = device.displayTemp()
				int_temp = int(temp)
				if (temp<0):
					command = "mplayer -framedrop ./lang/"+lang+"/minus.wav >> /dev/null"
				if((int_temp+0.5)<(temp-0.25)):
					filename = './lang/'+lang+'/'+`(int_temp+1)`+'.0.wav >>/dev/null'
				elif ((int_temp)>(temp-0.25)):
					filename = './lang/'+lang+'/'+`int_temp`+'.0.wav >> /dev/null' 
				else:
					filename = './lang/'+ lang + '/'+`int_temp`+'.5.wav >>/dev/null'	
				print filename
				command = "mplayer -framedrop "+ filename + " ./lang/" + lang + "/degree_celsius.wav >>/dev/null"
				os.system(command)
				displayFlag = 0
		sleep(0.1)
		#except KeyboardInterrupt:
		#	print "Exiting"
		#	device.displayBye()
		#	GPIO.cleanup()
#	except:
#		print "Exiting"
#		GPIO.cleanup()
main()	
