from PyQt5 import QtWidgets, QtGui, QtCore
from hardware_bridge.shot304_VISADriver import SHOT304VISADriver as SHOT304

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


        self.setLayout(grid_layout)

        # Connect buttons to functions
        self.up_button.clicked.connect(self.move_up)
        self.down_button.clicked.connect(self.move_down)
        self.left_button.clicked.connect(self.move_left)
        self.right_button.clicked.connect(self.move_right)
        self.z_up_button.clicked.connect(self.move_z_up)
        self.z_down_button.clicked.connect(self.move_z_down)
        self.axis_rotation_up_button.clicked.connect(self.move_axis_rotation_up)
        self.axis_rotation_down_button.clicked.connect(self.move_axis_rotation_down)

        self.setStyleSheet("""
            QWidget {
                background-color:rgb(4, 52, 99);
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
    
    def initialize(self): 
        self.shot304 = SHOT304("COM1")
        self.shot304.open_connection()

    def move_up(self):
        print("Moving up")

    def move_down(self):
        print("Moving down")

    def move_left(self):
        print("Moving left")

    def move_right(self):
        print("Moving right")
    
    def move_z_up(self):
        print("Moving Z up")
    def move_z_down(self):
        print("Moving Z down")
    def move_axis_rotation_up(self):
        print("Moving axis rotation up")
    def move_axis_rotation_down(self):
        print("Moving axis rotation down")

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MicroscopeControl()
    window.show()
    sys.exit(app.exec_())