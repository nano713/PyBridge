from PyQt5 import QtWidgets, QtGui, QtCore
from pybridge.hardware_bridge.shot304_VISADriver import SHOT304VISADriver as SHOT304
import logging 

logger = logging.getLogger(__name__)

class MicroscopeControl(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initialize()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle('Microscope Controller')
        self.setGeometry(100, 100, 400, 400)

        # Create a grid layout
        grid_layout = QtWidgets.QGridLayout()
        grid_layout_step = QtWidgets.QGridLayout()

        # Create arrow buttons
        self.up_button = QtWidgets.QPushButton('↑')
        self.down_button = QtWidgets.QPushButton('↓')
        self.left_button = QtWidgets.QPushButton('←')
        self.right_button = QtWidgets.QPushButton('→')

        self.z_up_button = QtWidgets.QPushButton('Z+')
        self.z_down_button = QtWidgets.QPushButton('Z-')

        self.axis_rotation_up_button = QtWidgets.QPushButton('AxisR+')
        self.axis_rotation_down_button = QtWidgets.QPushButton('AxisR-')

        # Set font size for buttons
        font = QtGui.QFont()
        font.setPointSize(20)
        self.up_button.setFont(font)
        self.down_button.setFont(font)
        self.left_button.setFont(font)
        self.right_button.setFont(font)
        self.z_up_button.setFont(font)
        self.z_down_button.setFont(font)
        self.axis_rotation_up_button.setFont(font)
        self.axis_rotation_down_button.setFont(font) 

        grid_layout.addWidget(self.up_button, 0, 1)
        grid_layout.addWidget(self.left_button, 1, 0)
        grid_layout.addWidget(self.right_button, 1, 2)
        grid_layout.addWidget(self.down_button, 2, 1)

        grid_layout.addWidget(self.z_up_button, 0, 3)
        grid_layout.addWidget(self.z_down_button, 2, 3)

        grid_layout.addWidget(self.axis_rotation_up_button, 0, 4)
        grid_layout.addWidget(self.axis_rotation_down_button, 2, 4)

        # #TODO: ADD A STEP SIZE INPUT BUTTON
        self.step_size_name = QtWidgets.QLabel('Step Size')
        self.step_size_input = QtWidgets.QDoubleSpinBox()
        self.step_size_input.setRange(1, 100000)
        self.step_size_input.setSingleStep(1) 
        self.step_size_input.setValue(10)
        grid_layout_step.addWidget(self.step_size_name, 3, 0)
        grid_layout_step.addWidget(self.step_size_input, 3, 1)
        grid_layout.addLayout(grid_layout_step, 3, 0, 1, 2)
        self.step_size_input.valueChanged.connect(self.update_step_size)



        # Connect buttons to functions
        self.up_button.clicked.connect(self.move_up)
        self.down_button.clicked.connect(self.move_down)
        self.left_button.clicked.connect(self.move_left)
        self.right_button.clicked.connect(self.move_right)
        self.z_up_button.clicked.connect(self.move_z_up)
        self.z_down_button.clicked.connect(self.move_z_down)
        self.axis_rotation_up_button.clicked.connect(self.move_axis_rotation_up)
        self.axis_rotation_down_button.clicked.connect(self.move_axis_rotation_down)


        self.setLayout(grid_layout)
        self.setLayout(grid_layout_step)

        self.setStyleSheet("""
            QWidget {
                background-color:rgb(4, 63, 122);
                color:rgb(148, 148, 152);
            }
            QLineEdit {
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 5px;
                background-color: #003366;
                color: #ffffff;
            }
            QPushButton {
                padding: 5px;
                background-color: #0078d7;
                color: #ffffff;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #005bb5;
            }
            QPushButton:pressed {
                background-color: #003f8a;
            }
        """)
    
    # def initialize(self): 
    #     self.shot304 = SHOT304("COM1")
    #     self.shot304.open_connection()
    def initialize(self):
        self.shot304 = SHOT304("ASRL3::INSTR")
        self.shot304.open_connection()
    def update_step_size(self, value):
        self.current_step_size = value
        print(f"Step size updated to {self.current_step_size}")

    def move_up(self):
        step_size = int(self.current_step_size)
        try:
            self.shot304.move_relative(step_size, 2)
            print(f"Move up {self.shot304.get_position(2)}")
        except Exception as e:
            print(f"Error moving up: {e}")
    def move_down(self):
        step_size =int(-self.step_size_input.value())
        try:
            self.shot304.move_relative(step_size, 2)
            print(f"Move down {self.shot304.get_position(2)}")
        except Exception as e:
            print(f"Error moving down: {e}") 

    def move_left(self):
        step_size = int(-self.current_step_size)
        try:
            self.shot304.move_relative(step_size, 1)
            print(f"Move left {self.shot304.get_position(1)}")
        except Exception as e:
            print(f"Error moving left: {e}")

    def move_right(self):
        step_size = int(self.current_step_size)
        try:
            self.shot304.move_relative(step_size, 1)
            print(f"Move right {self.shot304.get_position(1)}")
        except Exception as e:
            print(f"Error moving right: {e}")
    
    def move_z_up(self):
        step_size = int(self.current_step_size)
        try:
            self.shot304.move_relative(step_size, 3)
            print(f"Move Z axis up {self.shot304.get_position(3)}")
        except Exception as e:
            print(f"Error moving Z up: {e}")

    def move_z_down(self):
        step_size = int(-self.current_step_size)
        try:
            self.shot304.move_relative(step_size, 3)
            print(f"Move z axis down {self.shot304.get_position(3)}")
        except Exception as e:
            print(f"Error moving Z down: {e}")

    def move_axis_rotation_up(self):
        step_size = int(self.current_step_size)
        try:
            self.shot304.move_relative(step_size, 4)
            print("Rotation up")
        except Exception as e:
            print(f"Error moving axis rotation up: {e}")

    def move_axis_rotation_down(self):
        step_size =int(-self.current_step_size)
        try:
            self.shot304.move_relative(step_size, 4)
            print("Rotation down")
        except Exception as e:
            print(f"Error moving axis rotation down: {e}")

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MicroscopeControl()
    window.show()
    sys.exit(app.exec_())