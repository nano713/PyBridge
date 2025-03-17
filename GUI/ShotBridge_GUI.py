# GUI to control the microscope
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGridLayout, QLabel, QPushButton, QVBoxLayout, QWidget
from hardware_bridge.shot304_VISADriver import SHOT304VISADriver as SHOT304


class MicroscopeControl(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI() 
    
    def initUI(self):
        """ Initializes the GUI"""
        self.setGeometry(100, 100, 400, 200)
        self.setWindowTitle('Microscope Controller')
        layout = QtWidgets.QVBoxLayout()

        h_layout = QtWidgets.QHBoxLayout()
        


    
    def initialize(self):
        self.shot304 = SHOT304("ASRL3::INSTR")
       





