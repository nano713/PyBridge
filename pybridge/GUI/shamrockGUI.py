from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QComboBox, QHBoxLayout, QDialog
)
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLineEdit, QSpinBox
import sys
from pybridge.MoveBridge.shamorockBridge import SpectroGraphMoveBridge as Shamrock
from pybridge.ViewBridge.kymeraBridge import AndorIDUSViewerBridge as AndorIdus
 # import sdk2camera


class AndorIDusWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Andor iDus Camera")
        self.setGeometry(100, 100, 640,480)
        layout = QVBoxLayout()
        self.label = QLabel("Andor iDus Camera Control")
        layout.addWidget(self.label)
        self.setLayout(layout)
        
        self.connect_camera()
        self.initUI()
        
    def connect_camera(self):
        self.camera = AndorIdus(name="andor_camera")
        
    def initUI(self):
       layout = QVBoxLayout()
       self.num_images_label = QLabel("Number of Images:")
       self.num_images_input = QSpinBox()
       self.num_images_input.setRange(1, 100)
       layout.addWidget(self.num_images_label)
       layout.addWidget(self.num_images_input)
       self.timeout_label = QLabel("Timeout (s):")
       self.timeout_input = QLineEdit()
       layout.addWidget(self.timeout_label)
       layout.addWidget(self.timeout_input)
       self.setLayout(layout)

            

class LivePlotImageWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Live Plot Image")
        self.setGeometry(150,150,800,400)
        layout = QVBoxLayout()
        self.label = QLabel("Live Plot Image Control")
        layout.addWidget(self.label)
        self.setLayout(layout)

class ShamrockGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.shamrock = Shamrock(name = "shamrock")
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("Shamrock GUI")
        self.setGeometry(50, 50, 400,200)
        layout = QVBoxLayout()


        grating_layout = QHBoxLayout()
        self.grating_label = QLabel("Grating:")
        self.grating_combo = QComboBox()
        self.grating_combo.addItems(["Grating 1", "Grating 2", "Grating 3", "Grating 4"])
        grating_layout.addWidget(self.grating_label)
        grating_layout.addWidget(self.grating_combo)
        layout.addLayout(grating_layout)

        self.grating_button = QPushButton("Set Grating")
        self.grating_button.clicked.connect(self.set_grating)
        layout.addWidget(self.grating_button)

        self.take_spectrum_button = QPushButton("Take Spectrum")
        self.take_spectrum_button.clicked.connect(self.take_spectrum)
        layout.addWidget(self.take_spectrum_button)

        self.camera_button = QPushButton("Open Andor iDus Camera")
        self.camera_button.clicked.connect(self.open_camera) #Check this
        layout.addWidget(self.camera_button)

        self.live_plot_button = QPushButton("Open Live Plot Image")
        self.live_plot_button.clicked.connect(self.open_live_plot_image) #TODO 
        layout.addWidget(self.live_plot_button)

        self.setLayout(layout)
    def set_grating(self):
        try:
            self.shamrock.set_grating(self.grating_combo.currentText()) 
        except Exception as e:
            print(f"Error setting grating: {e}")
    def take_spectrum(self):
        try:
            spectrum = self.shamrock.take_spectrum()
            print("Spectrum taken:", spectrum)
        
        except Exception as e:
            print(f"Error taking spectrum: {e}")
    def open_camera(self):
        self.camera_window = AndorIDusWindow()
        self.camera_window.show()
    
    def open_live_plot_image(self):
        self.live_plot_image_window = LivePlotImageWindow()
        self.live_plot_image_window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    shamrock_gui = ShamrockGUI()
    shamrock_gui.show()
    sys.exit(app.exec_())