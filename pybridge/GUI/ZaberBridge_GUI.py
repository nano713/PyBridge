from PyQt5 import QtWidgets, QtCore
from pybridge.MoveBridge.zaberBridge_Connect import ZaberStage
from ophyd import Signal
import pyvisa
from pybridge.import_class import list_class, get_class

class MyWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.port = None
        self.zaber = ZaberStage(name='zaber')
        self.initUI()
    
    def initUI(self): 
        layout = QtWidgets.QVBoxLayout()

        # self.visa_name = QtWidgets.QLabel('Instrument Address:') 
        # self.visa_input = QtWidgets.QComboBox()
        # self.visa_input.addItems(self.rm.list_resources())
        # layout.addWidget(self.visa_name)
        # layout.addWidget(self.visa_input)

        # self.class_name = QtWidgets.QLabel('Instrument Class:')
        # self.class_input = QtWidgets.QComboBox() 
        # self.class_input.addItems(list_class("MoveBridge"))
        # self.class_input.currentTextChanged.connect(self.load_class)
        # layout.addWidget(self.class_name)
        # layout.addWidget(self.class_input)

        # self.unit_name = QtWidgets.QLabel('Unit:')
        # self.unit_input = QtWidgets.QComboBox()
        # self.unit_input.addItems(["um", "deg"])
        # layout.addWidget(self.unit_name)
        # layout.addWidget(self.unit_input)


        self.axis_name = QtWidgets.QLabel('Axis:')
        self.axis_index = self.zaber.get_axis_length()
        self.axis_input = QtWidgets.QComboBox()
        axis_list = [str(i + 1) for i in range(self.axis_index)]
        self.axis_input.addItems(axis_list)
        layout.addWidget(self.axis_name)
        layout.addWidget(self.axis_input)

        self.load_button = QtWidgets.QPushButton('Load Settings')
        self.load_button.clicked.connect(self.load_settings) 
        layout.addWidget(self.load_button)

        self.param_widgets = {}
        self.param_layout = QtWidgets.QFormLayout()
        for attr in dir(self.zaber):
            if hasattr(self.zaber, attr) and isinstance(getattr(self.zaber, attr), Signal):
                label = QtWidgets.QLabel(attr)
                value_label = QtWidgets.QLabel("^-^)/ <(Hello~)")
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
        self.setWindowTitle('Stage Actuator Zaber')
        self.show()
    def load_class(self): 
        class_name = self.class_input.currentText()
        self.zaber = get_class("hardware_interface", class_name)(name='zaber')
        self.load_settings()
        
    def load_settings(self):
        self.zaber.axis_index.put(int(self.axis_input.currentText()))
        self.zaber.get_position()
        self.update_values()
    
        # self.shrc.params['unit']['value'] = self.unit_input.currentText()
        # self.shrc.params['loop']['value'] = int(self.loop_input.currentText())
        # self.shrc.params['speed_ini']['value'] = self.speed_ini_input.value()
        # self.shrc.params['accel_t']['value'] = self.accel_t_input.value()
        # self.shrc.params['speed_fin']['value'] = self.speed_fin_input.value()
        # self.shrc.params['axis']['value'] = self.axis_input.currentText()
        # self.shrc.commit_settings()
        # self.update_values()
        # print('Settings loaded')

    def update_values(self):
        for attr, widget in self.param_widgets.items():
            try:
                value = getattr(self.zaber, attr).get()
                widget.setText(str(value))
            except Exception as e:
                # logger.error(f"Error reading {attr}: {e}")
                widget.setText("Error")


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    sys.exit(app.exec_())