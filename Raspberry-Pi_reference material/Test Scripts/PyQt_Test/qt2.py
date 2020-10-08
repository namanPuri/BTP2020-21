import sys
from PyQt4 import QtGui
app = QtGui.QApplication(sys.argv)
window = QtGui.QWidget()
window.setGeometry(0,0,640,480)
window.setWindowTitle("Hello World")
window.show()
app.exec_()
