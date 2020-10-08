#!/usr/bin/python

import sys
from time import sleep
from PyQt4 import QtGui, QtCore
from lm75 import LM75

class mainWindow(QtGui.QMainWindow):
	def __init__(self):
		super(mainWindow,self).__init__()
		self.setGeometry(0,0,300,200)
		self.setFixedSize(300,200)
		self.setWindowTitle("LM75 Temperature Sensor")
		
		quitBtn = QtGui.QPushButton("&Quit", self)
		quitBtn.resize(quitBtn.sizeHint())
		quitBtn.clicked.connect(self.close)
		quitBtn.move(100,150)
		
		self.tempLabel = QtGui.QLabel("Temperature : 0.0 C",self)
		self.tosLabel = QtGui.QLabel("Tos : 0.0 C",self)
		self.thysLabel = QtGui.QLabel("Thyst : 0.0 C",self)
		
		self.tempLabel.resize(self.tempLabel.sizeHint())
		self.tosLabel.resize(self.tosLabel.sizeHint())
		self.thysLabel.resize(self.thysLabel.sizeHint())
		
		self.tempLabel.move(50,10)
		self.tosLabel.move(50,60)
		self.thysLabel.move(50,110)
		
		self.sense = TempSensor(self)
		self.sense.active = True
		self.connect(self.sense,QtCore.SIGNAL("updateTemp(float,float,float)"),self.updateTemp)
		self.sense.start()
		
		self.show()
	def updateTemp(self,temp,tos,thys):
		tempdata = "Temperature : " + `temp` + " C"
		tosdata = "Tos : " + `tos` + " C"
		thysdata = "Thyst : " + `thys` + " C"
		self.tempLabel.setText(tempdata)
		self.tosLabel.setText(tosdata)
		self.thysLabel.setText(thysdata)
		self.tempLabel.resize(self.tempLabel.sizeHint())
		self.tosLabel.resize(self.tosLabel.sizeHint())
		self.thysLabel.resize(self.thysLabel.sizeHint())
	
	def close(self):
		self.sense.active = False 
		self.sense.quit()
		self.sense.wait()
		sys.exit(0)
	
		
class TempSensor(QtCore.QThread):
			active = False
			def __init__(self,parent=None):
				QtCore.QThread.__init__(self,parent)
				self.setTerminationEnabled(True)
				self.sensor = LM75(0x48)
				self.temp = ''
				self.tos = ''
				self.thys = ''
			def run(self):
				while self.active:
					self.temp = self.sensor.getTemp()
					self.tos = self.sensor.getTos()
					self.thys = self.sensor.getThys()
					self.emit(QtCore.SIGNAL("updateTemp(float, float, float)"),self.temp,self.tos, self.thys)
					sleep(0.1)

def main():	
	app = QtGui.QApplication(sys.argv)
	wind = mainWindow()
	app.exec_()
	
main()
