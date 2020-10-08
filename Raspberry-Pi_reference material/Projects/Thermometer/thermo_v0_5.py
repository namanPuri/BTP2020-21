#!/usr/bin/python

import sys
from time import sleep
from PyQt4 import QtGui, QtCore
from LM76 import LM76

class mainWindow(QtGui.QMainWindow):
	def __init__(self):
		super(mainWindow,self).__init__()
		self.setGeometry(0,0,300,200)
		self.setFixedSize(300,200)
		self.setWindowTitle("LM76 Temperature Sensor")
		quitBtn = QtGui.QPushButton("&Quit", self)
		quitBtn.resize(quitBtn.sizeHint())
		quitBtn.clicked.connect(self.close)
		quitBtn.move(100,150)		
		self.tempLabel = QtGui.QLabel("Temperature : 0.0 C",self)
		self.tempLabel.resize(self.tempLabel.sizeHint())		
		self.tempLabel.move(50,10)		
		self.sense = TempSensor(self)
		self.sense.active = True
		self.connect(self.sense,QtCore.SIGNAL("updateTemp(float)"),self.updateTemp)
		self.sense.start()
		self.show()
	
	def updateTemp(self,temp):
		tempdata = "Temperature : " + `temp` + " C"
		self.tempLabel.setText(tempdata)
		self.tempLabel.resize(self.tempLabel.sizeHint())
	
	def close(self):
		self.sense.active = False 
		self.sense.quit()
		self.sense.wait()
		sys.exit(0)
	
		
class TempSensor(QtCore.QThread):
			active = True
			def __init__(self,parent=None):
				QtCore.QThread.__init__(self,parent)
				self.setTerminationEnabled(True)
				self.sensor = LM76(0x48)
				self.temp = ''

			def run(self):
				while self.active:
					self.temp = self.sensor.getTemp()
					self.emit(QtCore.SIGNAL("updateTemp(float)"),self.temp)
					sleep(0.1)

def main():	
	app = QtGui.QApplication(sys.argv)
	wind = mainWindow()
	app.exec_()
	
main()
