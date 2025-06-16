from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QWidget, QPushButton, QLabel
import sys 


class KymeraGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kymera GUI")
        self.setGeometry(100, 100, 800, 600)
        self.initUI()
    
    def initUI(self):
        layoyt = QVBoxLayout()
        self.label = QLabel("Welcome to Kymera GUI", self)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setFont(QtGui.QFont("Arial", 24))
        
        