#!/usr/bin/python

import sys
import os
from PyQt4 import QtGui

class Window(QtGui.QMainWindow):
	
	def __init__(self):
		super(Window,self).__init__()
		self.setGeometry(50,50,300,200)
		self.setWindowTitle("OOP")
		self.show()
app = QtGui.QApplication(sys.argv)
wind = Window() 
app.exec_()
