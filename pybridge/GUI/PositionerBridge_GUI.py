import sys 
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont
from ChipPosition import SiChipPosition
from example_controller import MicroscopeControl

class Positioner_Matrix(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI() 
    
    def initUI(self):
        """ Initializes the GUI"""
        self.setGeometry(100, 100, 400, 200)
        self.setWindowTitle('Chip Positioner')
        layout = QtWidgets.QVBoxLayout()

        h_layout = QtWidgets.QHBoxLayout()
        h_layout.setSpacing(5)
        h_layout.setContentsMargins(0,0,0,0)

        self.x0_position = QtWidgets.QLabel('X0 Position:')
        self.x0_position.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.x0_input = QtWidgets.QDoubleSpinBox()
        self.x0_input.setRange(-999999999, 999999999)
        self.x0_input.setValue(0)
        self.x0_input.setDecimals(2)
        self.x0_input.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        h_layout.addWidget(self.x0_position)
        h_layout.addWidget(self.x0_input)

        self.y0_pos = QtWidgets.QLabel('Y0 Position:')
        self.y0_pos.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.y0_input = QtWidgets.QDoubleSpinBox()
        self.y0_input.setRange(-999999999, 999999999)
        self.y0_input.setValue(0)
        self.y0_input.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        h_layout.addWidget(self.y0_pos)
        h_layout.addWidget(self.y0_input)

        self.z0_pos = QtWidgets.QLabel('Z0 Position:')
        self.z0_pos.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed) 
        self.z0_input = QtWidgets.QDoubleSpinBox()
        self.z0_input.setRange(-999999999, 999999999)
        self.z0_input.setValue(0)
        self.z0_input.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        h_layout.addWidget(self.z0_pos)
        h_layout.addWidget(self.z0_input)

        layout.addLayout(h_layout)

        h1_layout = QtWidgets.QHBoxLayout()
        self.x1_pos = QtWidgets.QLabel('X1 Position:')
        self.x1_input = QtWidgets.QDoubleSpinBox()
        self.x1_input.setRange(-999999999, 999999999)
        self.x1_input.setValue(0)
        h1_layout.addWidget(self.x1_pos)
        h1_layout.addWidget(self.x1_input)

        self.y1_pos = QtWidgets.QLabel('Y1 Position:')
        self.y1_input = QtWidgets.QDoubleSpinBox() 
        self.y1_input.setRange(-999999999, 999999999)
        self.y1_input.setValue(0)
        h1_layout.addWidget(self.y1_pos)
        h1_layout.addWidget(self.y1_input)

        self.z1_pos = QtWidgets.QLabel('Z1 Position:')
        self.z1_input = QtWidgets.QDoubleSpinBox()
        self.z1_input.setRange(-999999999, 999999999)
        self.z1_input.setValue(0)
        h1_layout.addWidget(self.z1_pos)
        h1_layout.addWidget(self.z1_input)

        layout.addLayout(h1_layout)
        h2_layout = QtWidgets.QHBoxLayout()

        self.x2_pos = QtWidgets.QLabel('X2 Position:')
        self.x2_pos.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.x2_input = QtWidgets.QDoubleSpinBox()
        self.x2_input.setRange(-999999999, 999999999)
        self.x2_input.setValue(0)
        self.x2_input.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        h2_layout.addWidget(self.x2_pos)
        h2_layout.addWidget(self.x2_input)

        self.y2_pos = QtWidgets.QLabel('Y2 Position:')
        self.y2_pos.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.y2_input = QtWidgets.QDoubleSpinBox()
        self.y2_input.setRange(-999999999, 999999999)
        self.y2_input.setValue(0)
        self.y2_pos.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        h2_layout.addWidget(self.y2_pos)
        h2_layout.addWidget(self.y2_input)

        self.z2_pos = QtWidgets.QLabel('Z2 Position:')
        self.z2_pos.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.z2_input = QtWidgets.QDoubleSpinBox()
        self.z2_input.setRange(-999999999, 999999999)
        self.z2_input.setValue(0)
        self.z2_input.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        h2_layout.addWidget(self.z2_pos)
        h2_layout.addWidget(self.z2_input)

        layout.addLayout(h2_layout)

        h3_layout = QtWidgets.QHBoxLayout()
        self.x3_pos = QtWidgets.QLabel('X3 Position:')
        self.x3_pos.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.x3_input = QtWidgets.QDoubleSpinBox()
        self.x3_input.setRange(-999999999, 999999999)
        self.x3_input.setValue(0)
        self.x3_input.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        h3_layout.addWidget(self.x3_pos)
        h3_layout.addWidget(self.x3_input)

        self.y3_pos = QtWidgets.QLabel('Y3 Position:')
        self.y3_pos.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.y3_input = QtWidgets.QDoubleSpinBox()
        self.y3_input.setRange(-999999999, 999999999)
        self.y3_input.setValue(0)
        self.y3_input.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        h3_layout.addWidget(self.y3_pos)
        h3_layout.addWidget(self.y3_input)

        self.z3_pos = QtWidgets.QLabel('Z3 Position:')
        self.z3_pos.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.z3_input = QtWidgets.QDoubleSpinBox()
        self.z3_input.setRange(-999999999, 999999999)
        self.z3_input.setValue(0)
        self.z3_input.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        h3_layout.addWidget(self.z3_pos)
        h3_layout.addWidget(self.z3_input)

        layout.addLayout(h3_layout)

        self.compute_button = QtWidgets.QPushButton('Compute')
        self.compute_button.clicked.connect(self.compute)
        layout.addWidget(self.compute_button)

        self.result_box = QtWidgets.QLabel()
        self.result_box.setAlignment(QtCore.Qt.AlignCenter)
        self.result_box.setFont(QFont("Arial", 24, QFont.Bold))
        layout.addWidget(self.result_box)

        self.control_button = QtWidgets.QPushButton('Open Microscope Control')
        self.control_button.clicked.connect(self.open_microscope_control)
        layout.addWidget(self.control_button)

        self.setLayout(layout)
        self.show()
        self.setShortcutEnabled(True)
        
        self.setStyleSheet("""
            QWidget {
                background-color: rgb(30, 60, 100); /* Slightly lighter blue background */
                color: rgb(200, 200, 210); /* Light grey text */
            }
            QLineEdit {
                padding: 6px;
                border: 1px solid #5b718a;
                border-radius: 4px;
                background-color: #0e3a59;
                color: #e0e0e0;
                font-family: "Segoe UI";
                font-size: 12pt;
            }
            QPushButton {
                padding: 6px;
                background-color: #1077b1;
                color: #ffffff;
                border: none;
                border-radius: 4px;
                font-family: "Segoe UI Bold";
                font-size: 10pt;
            }
            QPushButton:hover {
                background-color: #0e5a8a;
            }
            QPushButton:pressed {
                background-color: #083a59;
            }
        """)
        layout_logo = QtWidgets.QVBoxLayout()
        self.logo = QtWidgets.QLabel()
        pixmap = self.logo.setPixmap(QPixmap('C:\\Users\\desha\\Downloads\\logo for nano_scan with stage, keithley, lock in amplifier, and spectrometer, illustration style, not too cartoon.png'))
        pixmap = self.logo.pixmap().scaled(200, 100, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        self.logo.setPixmap(pixmap)
        layout_logo.setAlignment(Qt.AlignCenter)
        layout.addLayout(layout_logo)

        header_logo = QtWidgets.QLabel("Welcome to Chip Positioner")
        header_logo.setFont(QFont("Arial", 20, QFont.Bold))
        header_logo.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(header_logo)

        self.add_shortcuts()
    
    def add_shortcuts(self):
        QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+Q"), self, self.close)
        QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+O"), self, self.open_microscope_control)
        QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+C"), self, self.compute)


    def load_settings(self):
        """ Loads the settings"""
        self.chip_position = SiChipPosition()
        self.x0 = self.x0_input.value()
        self.y0 = self.y0_input.value()
        self.z0 = self.z0_input.value()
        self.x1 = self.x1_input.value()
        self.y1 = self.y1_input.value()
        self.z1 = self.z1_input.value()
        self.x2 = self.x2_input.value()
        self.y2 = self.y2_input.value()
        self.z2 = self.z2_input.value()
        self.x3 = self.x3_input.value()
        self.y3 = self.y3_input.value()
        self.z3 = self.z3_input.value()
    def open_microscope_control(self): 
        self.microscope_control = MicroscopeControl()
        self.microscope_control.show()
    def compute(self): 
        """Computes the transformation matrix"""
        self.load_settings()
        transformation_matrix = self.chip_position.calculate_transformation_matrix(self.x0, self.y0, self.z0, self.x1, self.y1, self.z1, self.x2, self.y2, self.z2)
        matrix = self.chip_position.apply_transformation_matrix(transformation_matrix, self.x3, self.y3, self.z3) 
        self.result_box.setText(str(matrix))
            
if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = Positioner_Matrix()
    sys.exit(app.exec_())