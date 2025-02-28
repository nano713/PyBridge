from PyQt5 import QtWidgets, QtGui, QtCore
from MoveBridge.hardware_interface import SHRCStage
import logging
from ophyd import Signal
import pyvisa
from import_class import list_classes, get_class

class MyWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.rm = pyvisa.ResourceManager()
        self.shrc = SHRCStage(name='shrc203')
        self.initUI()
    
    def initUI(self): 
        layout = QtWidgets.QVBoxLayout()

        self.visa_name = QtWidgets.QLabel('Instrument Address:') 
        self.visa_input = QtWidgets.QComboBox()
        self.visa_input.addItems(self.rm.list_resources())
        layout.addWidget(self.visa_name)
        layout.addWidget(self.visa_input)

        self.class_name = QtWidgets.QLabel('Instrument Class:')
        self.class_input = QtWidgets.QComboBox() 
        self.class_input.addItems(list_classes("MoveBridge"))
        self.class_input.currentTextChanged.connect(self.load_class)
        layout.addWidget(self.class_name)
        layout.addWidget(self.class_input)

        self.unit_name = QtWidgets.QLabel('Unit:')
        self.unit_input = QtWidgets.QComboBox()
        self.unit_input.addItems(["um", "mm", "nm", "deg", "pulse"])
        layout.addWidget(self.unit_name)
        layout.addWidget(self.unit_input)

        self.loop_name = QtWidgets.QLabel('Loop:')
        self.loop_input = QtWidgets.QComboBox()
        self.loop_input.addItems(["0", "1"])
        self.loop_input.currentTextChanged.connect(self.load_settings)
        layout.addWidget(self.loop_name)
        layout.addWidget(self.loop_input)

        self.speed_ini_name = QtWidgets.QLabel('Speed Initial:')
        self.speed_ini_input = QtWidgets.QDoubleSpinBox()
        self.speed_ini_input.setRange(0, 100000)
        self.speed_ini_input.setValue(2000)
        self.speed_ini_input.valueChanged.connect(self.load_settings)
        layout.addWidget(self.speed_ini_name)
        layout.addWidget(self.speed_ini_input)

        self.accel_t_name = QtWidgets.QLabel('Acceleration Time:')   
        self.accel_t_input = QtWidgets.QDoubleSpinBox()
        self.accel_t_input.setRange(0, 100000)
        self.accel_t_input.setValue(100)
        layout.addWidget(self.accel_t_name)
        layout.addWidget(self.accel_t_input)

        self.speed_fin_name = QtWidgets.QLabel('Speed Final:')
        self.speed_fin_input = QtWidgets.QDoubleSpinBox()
        self.speed_fin_input.setRange(0, 100000)
        self.speed_fin_input.setValue(20000)
        layout.addWidget(self.speed_fin_name)
        layout.addWidget(self.speed_fin_input)

        self.axis_name = QtWidgets.QLabel('Axis:')
        self.axis_input = QtWidgets.QComboBox()
        self.axis_input.addItems(["X", "Y", "Z"])
        layout.addWidget(self.axis_name)
        layout.addWidget(self.axis_input)

        self.load_button = QtWidgets.QPushButton('Load Settings')
        self.load_button.clicked.connect(self.load_settings) # DK - AttributeError: 'MyWindow' object has no attribute 'load_settings'
        layout.addWidget(self.load_button)

        self.param_widgets = {}
        self.param_layout = QtWidgets.QFormLayout()
        for attr in dir(self.shrc):
            if isinstance(getattr(self.shrc, attr), Signal):
                label = QtWidgets.QLabel(attr)
                value_label = QtWidgets.QLabel("^-^")
                self.param_widgets[attr] = value_label
                self.param_layout.addRow(label, value_label)
        layout.addLayout(self.param_layout)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_values)
        self.timer.start(1000)
        # self.commit_button = QtWidgets.QPushButton('Commit Settings')
        # self.commit_button.clicked.connect(self.commit_settings)
        # layout.addWidget(self.commit_button)

        self.setLayout(layout)
        self.setWindowTitle('Stage Controller SHRC')
        self.show()
    def load_class(self): 
        class_name = self.class_input.currentText()
        self.shrc = get_class("hardware_interface", class_name)(name='shrc203')
        self.update_param_widgets()
        
    def load_settings(self): 
    
        self.shrc.params['unit']['value'] = self.unit_input.currentText()
        self.shrc.params['loop']['value'] = int(self.loop_input.currentText())
        self.shrc.params['speed_ini']['value'] = self.speed_ini_input.value()
        self.shrc.params['accel_t']['value'] = self.accel_t_input.value()
        self.shrc.params['speed_fin']['value'] = self.speed_fin_input.value()
        self.shrc.params['axis']['value'] = self.axis_input.currentText()
        self.shrc.commit_settings()
        self.update_values()
        print('Settings loaded')

    def update_values(self):
        for attr, widget in self.param_widgets.items():
            try:
                value = getattr(self.shrc, attr).get()
                widget.setText(str(value))
            except Exception as e:
                # logger.error(f"Error reading {attr}: {e}")
                widget.setText("Error")


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    sys.exit(app.exec_())