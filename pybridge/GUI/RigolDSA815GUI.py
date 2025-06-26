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
        
        set_button = QtWidgets.QPushButton("Set Parameters")
        set_button.clicked.connect(self.set_parameters)
        layout.addWidget(set_button)
        
        plot_button = QtWidgets.QPushButton("Plot Spectrum")
        plot_button.clicked.connect(self.plot_spectrum)
        
        
        layout.addWidget(plot_button)
        
        self.figure = Figure(figsize=(8, 6))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        self.setLayout(layout)
        
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
    
    def set_parameters(self):
        self.rigol.set_center_frequency(self.center_freq_input.text())
        self.rigol.set_start_frequency(self.start_freq_input.text())
        self.rigol.set_stop_frequency(self.stop_freq_input.text())
        self.rigol.set_sweep_time(self.sweep_time_input.text())
        self.rigol.set_frequency_step(self.frequency_step_input.text())
    
    def plot_spectrum(self):
        freq = self.rigol.get_frequencies()
        data = self.rigol.get_trigger_data()
        
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.plot(freq, data)
        ax.set_title("Spectrum Plot")
        ax.set_xlabel("Frequency (Hz)")
        ax.set_ylabel("Amplitude (dBm)")
        ax.grid(True)
        self.canvas.draw()
        

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    instru = DSA815ViewBridge(name = "DSA815",driver="USB0::0x1AB1::0x0960::DSA8A154202508::INSTR")
    gui = DSA815GUI(instru)
    gui.initUI()
    gui.show()
    sys.exit(app.exec_())