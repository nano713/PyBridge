from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QWidget
from pybridge.ViewBridge.dsa815Bridge import DSA815ViewBridge
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class DSA815GUI(QWidget):
    
    def __init__(self, instru: DSA815ViewBridge):
        super().__init__()
        self.rigol = instru
        self.setWindowTitle("DSA815 Spectrum Analyzer")
        self.setGeometry(100, 200, 800, 600)
        
    def initUI(self):
        layout = QVBoxLayout()
        
        
        frequency_layout = QtWidgets.QHBoxLayout()
        self.start_freq_input = QtWidgets.QLineEdit()
        self.start_freq_input.setPlaceholderText("Start Frequency (Hz)")
        
        self.stop_freq_input = QtWidgets.QLineEdit()
        self.stop_freq_input.setPlaceholderText("Stop Frequency (Hz)")
        
        self.center_freq_input = QtWidgets.QLineEdit()
        self.center_freq_input.setPlaceholderText("Center Frequency (Hz)")
        
        frequency_layout.addWidget(self.start_freq_input)
        frequency_layout.addWidget(self.stop_freq_input)
        frequency_layout.addWidget(self.center_freq_input)
        layout.addLayout(frequency_layout)
        
        sweep_layout = QtWidgets.QHBoxLayout()
        self.sweep_time_input = QtWidgets.QLineEdit()
        self.sweep_time_input.setPlaceholderText("Sweep Time (s)")
        self.frequency_step_input = QtWidgets.QLineEdit()
        self.frequency_step_input.setPlaceholderText("Frequency Step (Hz)")
        sweep_layout.addWidget(self.sweep_time_input)
        sweep_layout.addWidget(self.frequency_step_input)
        layout.addLayout(sweep_layout)
        
        # set_button = QtWidgets.QPushButton("Set Parameters")
        # set_button.clicked.connect(self.set_parameters)
        # layout.addWidget(set_button)
        
        # plot_button = QtWidgets.QPushButton("Plot Spectrum")
        # plot_button.clicked.connect(self.plot_spectrum)
        
        
        # layout.addWidget(plot_button)
        
        self.figure = Figure(figsize=(8, 6))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        self.setLayout(layout)
    
    def set_parameters(self):
        pass

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    instru = DSA815ViewBridge(name = "DSA815",driver="USB0::0x1AB1::0x0960::DSA8A154202508::INSTR")
    gui = DSA815GUI(instru)
    gui.initUI()
    gui.show()
    sys.exit(app.exec_())