#!/usr/bin/python

import sys
import os
from PyQt4 import QtGui,QtCore

class Window(QtGui.QMainWindow):
	
	def __init__(self):
		super(Window,self).__init__()
		self.setGeometry(50,50,300,200)
		self.setWindowTitle("OOP")
		self.home()
		
	def home(self):
		btn = QtGui.QPushButton("Quit",self)
		btn.resize(100,100)
		btn.move(100,100)
		btn.clicked.connect(QtCore.QCoreApplication.instance().quit)
		self.show()
def main():
	app = QtGui.QApplication(sys.argv)
	wind = Window() 
	sys.exit(app.exec_())

main()
