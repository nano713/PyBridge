from PyQt5 import QtWidgets, QtGui, QtCore

class RemoteControl(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle('Remote Control')
        self.setGeometry(100, 100, 300, 300)

        # Create a grid layout
        grid_layout = QtWidgets.QGridLayout()

        # Create arrow buttons
        self.up_button = QtWidgets.QPushButton('↑')
        self.down_button = QtWidgets.QPushButton('↓')
        self.left_button = QtWidgets.QPushButton('←')
        self.right_button = QtWidgets.QPushButton('→')

        # Set font size for buttons
        font = QtGui.QFont()
        font.setPointSize(20)
        self.up_button.setFont(font)
        self.down_button.setFont(font)
        self.left_button.setFont(font)
        self.right_button.setFont(font)

        # Add buttons to the grid layout
        grid_layout.addWidget(self.up_button, 0, 1)
        grid_layout.addWidget(self.left_button, 1, 0)
        grid_layout.addWidget(self.right_button, 1, 2)
        grid_layout.addWidget(self.down_button, 2, 1)

        # Set layout
        self.setLayout(grid_layout)

        # Connect buttons to functions
        self.up_button.clicked.connect(self.move_up)
        self.down_button.clicked.connect(self.move_down)
        self.left_button.clicked.connect(self.move_left)
        self.right_button.clicked.connect(self.move_right)

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

    def move_up(self):
        print("Moving up")

    def move_down(self):
        print("Moving down")

    def move_left(self):
        print("Moving left")

    def move_right(self):
        print("Moving right")

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = RemoteControl()
    window.show()
    sys.exit(app.exec_())