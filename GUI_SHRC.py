from pyqt5 import QtWidgets, QtGui, QtCore
from hardware_interface import SHRCStage

class MyWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.stage = SHRCStage()
    
    def initUI(self): 
        layout = QtWidgets.QVBoxLayout()

        self.visa_name = QtWidgets.QLineEdit('Instrument Address:') 
        self.visa_input = QtWidgets.QLineEdit()
        layout.addWidget(self.visa_name)
        layout.addWidget(self.visa_input)

        self.unit_name = QtWidgets.QLineEdit('Unit:')
        self.unit_input = QtWidgets.QComboBox()
        self.unit_input.addItems(["um", "mm", "nm", "deg", "pulse"])
        layout.addWidget(self.unit_name)
        layout.addWidget(self.unit_input)

        self.loop_name = QtWidgets.QLineEdit('Loop:')
        self.loop_input = QtWidgets.QSpinBox()
        layout.addWidget(self.loop_name)
        layout.addWidget(self.loop_input)

        self.speed_ini_name = QtWidgets.QLineEdit('Speed Initial:')

