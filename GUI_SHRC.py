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
        self.speed_ini_input = QtWidgets.QDoubleSpinBox()
        layout.addWidget(self.speed_ini_name)
        layout.addWidget(self.speed_ini_input)

        self.accel_t_name = QtWidgets.QLineEdit('Acceleration Time:')   
        self.accel_t_input = QtWidgets.QDoubleSpinBox()
        layout.addWidget(self.accel_t_name)
        layout.addWidget(self.accel_t_input)

        self.speed_fin_name = QtWidgets.QLineEdit('Speed Final:')
        self.speed_fin_input = QtWidgets.QDoubleSpinBox()
        layout.addWidget(self.speed_fin_name)
        layout.addWidget(self.speed_fin_input)

        self.axis_name = QtWidgets.QLineEdit('Axis:')
        self.axis_input = QtWidgets.QComboBox()
        self.axis_input.addItems(["X", "Y", "Z"])
        layout.addWidget(self.axis_name)
        layout.addWidget(self.axis_input)

        self.load_button = QtWidgets.QPushButton('Load Settings')
        self.load_button.clicked.connect(self.load_settings)
        layout.addWidget(self.load_button)

        self.commit_button = QtWidgets.QPushButton('Commit Settings')
        self.commit_button.clicked.connect(self.commit_settings)
        layout.addWidget(self.commit_button)

        self.setLayout(layout)
        self.setWindowTitle('Stage Controller SHRC')
        self.show()


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    sys.exit(app.exec_())