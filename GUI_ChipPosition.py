from PyQt5 import QtWidgets, QtGui, QtCore
from MoveBridge.hardware_interface import SHRCStage
import logging
from ophyd import Signal
import pyvisa

class MyWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI() 
    
    def initUI(self):
        """ Initializes the GUI"""
        self.setGeometry(100, 100, 400, 200)
        self.setWindowTitle('Chip Positioner')
        layout = QtWidgets.QVBoxLayout()

        h_layout = QtWidgets.QHBoxLayout()
        self.x0_position = QtWidgets.QLabel('X0 Position:')
        self.x0_input = QtWidgets.QDoubleSpinBox()
        self.x0_input.setRange(-100, 100)
        self.x0_input.setValue(0)
        h_layout.addWidget(self.x0_position)
        h_layout.addWidget(self.x0_input)

        self.y0_pos = QtWidgets.QLabel('Y0 Position:')
        self.y0_input = QtWidgets.QDoubleSpinBox()
        self.y0_input.setRange(-100, 100) 
        self.y0_input.setValue(0)
        h_layout.addWidget(self.y0_pos)
        h_layout.addWidget(self.y0_input)

        self.z0_pos = QtWidgets.QLabel('Z0 Position:') 
        self.z0_input = QtWidgets.QDoubleSpinBox()
        self.z0_input.setRange(-100, 100)
        self.z0_input.setValue(0)
        h_layout.addWidget(self.z0_pos)
        h_layout.addWidget(self.z0_input)

        layout.addLayout(h_layout)

        h1_layout = QtWidgets.QHBoxLayout()
        self.x1_pos = QtWidgets.QLabel('X1 Position:')
        self.x1_input = QtWidgets.QDoubleSpinBox()
        self.x1_input.setRange(-100, 100)
        self.x1_input.setValue(0)
        h1_layout.addWidget(self.x1_pos)
        h1_layout.addWidget(self.x1_input)

        self.y1_pos = QtWidgets.QLabel('Y1 Position:')
        self.y1_input = QtWidgets.QDoubleSpinBox() 
        self.y1_input.setRange(-100, 100)
        self.y1_input.setValue(0)
        h1_layout.addWidget(self.y1_pos)
        h1_layout.addWidget(self.y1_input)

        self.z1_pos = QtWidgets.QLabel('Z1 Position:')
        self.z1_input = QtWidgets.QDoubleSpinBox()
        self.z1_input.setRange(-100, 100)
        self.z1_input.setValue(0)
        h1_layout.addWidget(self.z1_pos)
        h1_layout.addWidget(self.z1_input) 

        layout.addLayout(h1_layout)

        self.compute_button = QtWidgets.QPushButton('Compute')
        # self.compute_button.clicked.connect(self.compute)
        layout.addWidget(self.compute_button)

        self.setLayout(layout)
        self.show()

        def load_settings(self): 
            """ Loads the settings"""
            self.x0 = self.x0_input.currentText()
            self.y0 = self.y0_input.currentText()
            self.z0 = self.z0_input.currentText()
            self.x1 = self.x1_input.currentText()
            self.y1 = self.y1_input.currentText()
            self.z1 = self.z1_input.currentText()

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    sys.exit(app.exec_())