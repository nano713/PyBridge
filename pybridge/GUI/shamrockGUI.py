from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QComboBox, QHBoxLayout, QDialog
)
from PyQt5.QtCore import Qt
from pybridge.MoveBridge.shamorockBridge import ShamrockBridge as Shamrock
# import sdk2camera
import sys

class AndorIDusWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Andor iDus Camera")
        self.setGeometry(100, 100, 640,480)
        layout = QVBoxLayout()
        self.label = QLabel("Andor iDus Camera Control")
        layout.addWidget(self.label)
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
        pass 


if __name__ == "__main__":
    app = QApplication(sys.argv)
    shamrock_gui = ShamrockGUI()
    shamrock_gui.show()
    andor_idus_window = AndorIDusWindow()
    live_plot_image_window = LivePlotImageWindow()
    sys.exit(app.exec_())