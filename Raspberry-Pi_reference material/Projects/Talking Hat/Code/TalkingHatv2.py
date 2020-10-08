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
import threading
import re
import datetime

time = 0
temp = 0
READY = 4
langIndex = 0
langList = 0
lang = 0 
displayFlag = 0

class Sensors(threading.Thread):
        def __init__(self):
                threading.Thread.__init__(self)
                self.tempSensor = LM75(0x48)
		#self.timeSensor = PCF8563.PCF8563(1,0x51)
        
	def run(self):
		while True:
                	temp = self.tempSensor.LM75.getTemp()
			#time = `self.timeSensor._read_hours()`+':'+`self.timeSensor._read_minutes()`+':'+`self.timeSensor._read_seconds()		
			time = datetime.datetime.now().strftime("%H:%M:%S")
			print "Thread : Sensors"

class Switches(threading.Thread):
	def __init__(self,displayLCD):
		threading.Thread.__init__(self)
		self.LANG = 17
		self.SPEAK = 26
		GPIO.setup(self.LANG,GPIO.IN)
		GPIO.setup(self.SPEAK,GPIO.IN)
		self.display = displayLCD
			
	def run(self):
		while True:
			if (GPIO.input(self.LANG) == False):
				sleep(0.01)
				if (GPIO.input(self.LANG)==FALSE):
					langIndex = langIndex + 1
					if langIndex >= len(langList):
						langIndex = 0 					
					lang = langList[langIndex]
					command = "mplayer ./lang/support/" + langList[langIndex] + ".wav >>/dev/null"
                                	os.system(command)
			if (GPIO.input(self.SPEAK) == False):
                                sleep(0.01)
                                if (GPIO.input(self.SPEAK)==FALSE):
					displayFlag = 1
					self.display.displayTemp()
					self.int_temp = int(temp)
					if (temp<0):
						command = "mplayer -framedrop ./lang/"+lang+"/minus.wav >> /dev/null"
					if((self.int_temp+0.5)<(temp-0.25)):
						filename = "./lang/"+lang+"/"+`self.int_temp+1` + ".0.wav >>/dev/null"
					elif ((self.int_temp)>(temp-0.25)):
						filename = "./lang/"+lang+"/"+`self.int_temp` +".0.wav >> /dev/null"
					else:
						filename = "./lang/"+lang+"/"+`self.int_temp`+".5.wav >>/dev/null"	
					command = "mplayer -framedrop "+ filename + " ./lang/" + lang + "/degree_celsius.wav >>/dev/null"
					os.system(command)
					displayFlag = 0
class displayLCD():
	def __init__(self):
		self.LCD_DC = 5
		self.LCD_BL = 6
		self.LCD_RST = 22
		self.tempSensor = LM75(0x48)
		self.rtcSensor = 0 #incorporate rtc here
		self.time = '00:00:00'
		self.temp = '0'		

	def beginLCD(self):
		GPIO.setup(self.LCD_BL,GPIO.OUT)
		GPIO.output(self.LCD_BL,GPIO.HIGH)
		self.Display = LCD.PCD8544(self.LCD_DC,self.LCD_RST, spi=SPI.SpiDev(0,0,max_speed_hz=4000000))
		self.Display.begin(contrast=60)
		self.image =  Image.new('1',(LCD.LCDWIDTH,LCD.LCDHEIGHT))
                self.draw = ImageDraw.Draw(self.image)
		self.Display.clear()
		self.Display.display()

	def clearImage(self):
		self.draw.rectangle((0,0,LCD.LCDWIDTH,LCD.LCDHEIGHT),outline=255,fill=255)
		self.Display.image(self.image)
		self.Display.display()

	def welcomeMessage(self):
		self.clearImage()
		self.draw.rectangle((0,0,LCD.LCDWIDTH,LCD.LCDHEIGHT),outline=255, fill = 255)
		self.font = ImageFont.truetype('Lady Radical.ttf', 16)
		self.draw.text((6,2),'Welcome',font=self.font)
		self.draw.text((32,14),'to',font=self.font)
		self.draw.text((2,27),'Talking Hat',font=self.font)
		self.Display.image(self.image)
		self.Display.display() 

	def displayTime(self):
		self.clearImage()
		self.draw.text((25,0),'Time',font=self.font)
		self.time = datetime.datetime.now().strftime("%H:%M:%S")
		self.draw.text((20,20),self.time,font=self.font)
                #self.draw.text((15,30),'',font=self.font)
                self.Display.image(self.image)
                self.Display.display()

	def displayTemp(self):
		self.clearImage()
		self.temp=self.tempSensor.getTemp()
		self.draw.text((2,0),'Temperature',font=self.font)
		self.draw.text((35,15),`self.temp`,font=self.font)
		self.draw.text((15,30),'Celsius',font=self.font)
		self.Display.image(self.image)
		self.Display.display()						
		
def main():
	#Preparing the GPIO
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(READY, GPIO.OUT)
	GPIO.output(READY,GPIO.LOW)
	
	#Prepare the Language List
#	langList = os.listdir('./lang/support')
#	for index in range(len(langList)):
#		langList[index] = langList[index][:-4]
#	langIndex = 0
	
	#Initialization
	device = displayLCD()
	device.beginLCD()
	device.welcomeMessage()
	#sensor = Sensors()
	#sensor.start()
	GPIO.output(READY,GPIO.HIGH)
	sleep(1)
	try:
		while True:
			device.displayTime()
			sleep(0.05)
	except KeyboardInterrupt:
		print "Exiting.."
	#	sensor.join()
#	GPIO.cleanup()
main()	
