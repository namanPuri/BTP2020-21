#!/usr/bin/python

import sys
import os
from PyQt4 import QtGui,QtCore

class Window(QtGui.QMainWindow):
	
	def __init__(self):
		super(Window,self).__init__()
		self.setGeometry(50,50,300,200)
		self.setWindowTitle("OOP")
		
		extractAction = QtGui.QAction("&Menu Bar",self)
		extractAction.setShortcut("Ctrl+Q")
		extractAction.setStatusTip('exiting')
		extractAction.triggered.connect(self.close_application)
		
		self.statusBar()
		
		mainMenu = self.menuBar()
		fileMenu = mainMenu.addMenu("&File")
		fileMenu.addAction(extractAction)
		
		self.home()
		
	def home(self):
		btn = QtGui.QPushButton("Quit",self)
		btn.resize(btn.minimumSizeHint())
		btn.move(100,100)
		btn.clicked.connect(self.close_application)
		self.show()

	def close_application(self):
		print "Exiting"
		sys.exit()
def main():
	app = QtGui.QApplication(sys.argv)
	wind = Window() 
	sys.exit(app.exec_())

main()
