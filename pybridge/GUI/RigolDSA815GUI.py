from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QWidget, QHBoxLayout, QLabel
from pybridge.ViewBridge.dsa815Bridge import DSA815ViewBridge
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import os
from datetime import datetime

class DSA815GUI(QWidget):
    
    def __init__(self, instru: DSA815ViewBridge):
        super().__init__()
        self.rigol = instru
        self.setWindowTitle("DSA815 Spectrum Analyzer")
        self.setGeometry(100, 200, 800, 600)
        self.save_directory = os.getcwd()  # Default to current working directory
        
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
        
        directory_layout = QtWidgets.QHBoxLayout()
        self.directory_label = QLabel(f"Save Directory: {self.save_directory}")
        self.directory_label.setWordWrap(True)
        directory_button = QtWidgets.QPushButton("Choose Directory")
        directory_button.clicked.connect(self.choose_directory)
        directory_layout.addWidget(self.directory_label, 1)  
        directory_layout.addWidget(directory_button)
        layout.addLayout(directory_layout)
        
        set_button = QtWidgets.QPushButton("Set Parameters")
        set_button.clicked.connect(self.set_parameters)
        layout.addWidget(set_button)
        
        plot_button = QtWidgets.QPushButton("Plot Spectrum")
        plot_button.clicked.connect(self.plot_spectrum)
        
        
        layout.addWidget(plot_button)
        

        save_button = QtWidgets.QPushButton("Save Data")
        save_button.clicked.connect(self.save_data)
        layout.addWidget(save_button)
        
    
        
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
            QLabel {
                padding: 5px;
                color: #ffffff;
                font-size: 10px;
            }
        """)
    
    def set_parameters(self):
        self.rigol.set_center_frequency(self.center_freq_input.text())
        self.rigol.set_start_frequency(self.start_freq_input.text())
        self.rigol.set_stop_frequency(self.stop_freq_input.text())
        self.rigol.set_sweep_time(self.sweep_time_input.text())
        self.rigol.set_frequency_step(self.frequency_step_input.text())
    
    def choose_directory(self):
        """Open a dialog to choose the save directory"""
        directory = QtWidgets.QFileDialog.getExistingDirectory(
            self, 
            "Choose Save Directory", 
            self.save_directory
        )
        if directory:
            self.save_directory = directory
            self.directory_label.setText(f"Save Directory: {self.save_directory}")
    
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
    def save_data(self):
        """Save data to the selected directory"""
        try:
            # Get current data
            freq = self.rigol.get_frequencies()
            data = self.rigol.get_trigger_data()
            
            if freq is None or data is None or len(freq) == 0 or len(data) == 0:
                QtWidgets.QMessageBox.warning(self, "No Data", "No data available to save. Please plot spectrum first.")
                return
            

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            default_filename = f"spectrum_data_{timestamp}.csv"
            
            default_path = os.path.join(self.save_directory, default_filename)
            
            filename, _ = QtWidgets.QFileDialog.getSaveFileName(
                self, 
                "Save Data", 
                default_path, 
                "CSV Files (*.csv);;All Files (*)"
            )
            
            if filename:
                self.save_directory = os.path.dirname(filename)
                self.directory_label.setText(f"Save Directory: {self.save_directory}")
                
                self.rigol.save_data(filename)
                
                data_points = min(len(freq), len(data))
                freq_range = f"{freq[0]:.2e} Hz to {freq[-1]:.2e} Hz" if len(freq) > 1 else f"{freq[0]:.2e} Hz"
                
                QtWidgets.QMessageBox.information(
                    self, 
                    "Success", 
                    f"Data saved successfully!\n\n"
                    f"File: {os.path.basename(filename)}\n"
                    f"Location: {os.path.dirname(filename)}\n"
                    f"Data points: {data_points}\n"
                    f"Frequency range: {freq_range}"
                )
            else:
                QtWidgets.QMessageBox.warning(self, "Cancelled", "Save operation cancelled.")
                
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Failed to save data:\n{str(e)}")
        

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    instru = DSA815ViewBridge(name = "DSA815",driver="USB0::0x1AB1::0x0960::DSA8A154202508::INSTR")
    gui = DSA815GUI(instru)
    gui.initUI()
    gui.show()
    sys.exit(app.exec_())