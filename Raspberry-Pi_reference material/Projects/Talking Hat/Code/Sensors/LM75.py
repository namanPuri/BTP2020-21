#!/usr/bin/python
import smbus

class LM75():
	bus = smbus.SMBus(1)
	address = 0x48 
	def __init__(self,add):
		self.address = add
		self.setConf(0x00)
		self.setThys(0x004B)
		self.setTos(0x0050)
		#self.setConf(0x00)
		return
	def getTemp(self):
		temp = self.bus.read_word_data(self.address,0x00)
		dec = (temp&0x8000)>>15
		temsign = temp & 0x0080
		temp = temp&0x007F
		temp = ((-1)**temsign)*( temp +(0.5*dec))
		return temp
	def getThys(self):
		thys = self.bus.read_word_data(self.address,0x02)
                dec = (thys&0x8000)>>15
		thyssign = thys & 0x0080
                thys = thys&0x007F
                thys = ((-1)**thyssign)*( thys +(0.5*dec))              
                return thys
	def getTos(self):
                tos = self.bus.read_word_data(self.address,0x03)
                dec = (tos&0x8000)>>15
                tossign = tos & 0x0080
                tos = tos&0x007F
                tos = ((-1)**tossign)*( tos +(0.5*dec))
                return tos
	def getConf(self):
		conf  = self.bus.read_byte_data(self.address,0x01)
		return bin(conf)
	def setConf(self,conf):
		self.bus.write_byte_data(self.address,0x01,conf)
		return
	def setThys(self,thys):
		self.bus.write_word_data(self.address,0x02,thys)
		return
	def setTos(self,tos):
                self.bus.write_word_data(self.address,0x03,tos)
                return
	
