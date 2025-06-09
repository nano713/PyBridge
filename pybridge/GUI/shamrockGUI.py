from PyQt5.QtWidgets import (
        QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QCheckBox, QComboBox, QHBoxLayout, QDialog, QGroupBox, QFileDialog
    )
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLineEdit, QSpinBox
import sys
from matplotlib.figure import Figure
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from pybridge.MoveBridge.shamorockBridge import SpectroGraphMoveBridge as Shamrock
from pybridge.ViewBridge.kymeraBridge import AndorIDUSViewerBridge as AndorIdus


class AndorIDusWindow(QDialog):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("Andor iDus Camera")
            self.setGeometry(100, 100, 640,480)
            # layout = QVBoxLayout()
            # self.label = QLabel("Andor iDus Camera Control")
            # # layout.addWidget(self.label)
            # self.setLayout(layout)
            
            # self.connect_camera()
            self.initUI()
            self.connect_camera()
            self.image_data = []
            self.canvas = None
            
        def connect_camera(self):
           
             self.camera = AndorIdus(name = "Andor iDus Camera")
             if not self.camera.is_connected():
                print("Connecting to Andor iDus Camera...")
                self.camera.connect()
                if not self.camera.is_connected():
                    print("Failed to connect to Andor iDus Camera.")
                    return
        def initUI(self):
            main_layout = QVBoxLayout()
            self.label = QLabel("Andor iDus Camera Control")
            main_layout.addWidget(self.label)
            
            controls_group = QGroupBox("Image Acquisition")
            controls_layout = QVBoxLayout()


            self.num_images_label = QLabel("Number of Images:")
            self.num_images_input = QSpinBox()
            self.num_images_input.setRange(1, 100)
            controls_layout.addWidget(self.num_images_label)
            controls_layout.addWidget(self.num_images_input)

            self.timeout_label = QLabel("Timeout (s):")
            self.timeout_input = QLineEdit()
            self.timeout_input.setText("10")
            controls_layout.addWidget(self.timeout_label)
            controls_layout.addWidget(self.timeout_input)
            
            self.exposure_time_label = QLabel("Exposure Time (ms):")
            self.exposure_time_input = QLineEdit()
            self.exposure_time_input.setText("100")
            controls_layout.addWidget(self.exposure_time_label)
            controls_layout.addWidget(self.exposure_time_input)
            
            self.set_directory_button = QPushButton("Set Directory")
            self.set_directory_button.clicked.connect(self.set_directory)
            controls_layout.addWidget(self.set_directory_button)
            
            self.multiple_images_checkbox = QCheckBox("Multiple Images")
            self.multiple_images_checkbox.setChecked(True)
            controls_layout.addWidget(self.multiple_images_checkbox)
            
            self.figure = Figure(figsize = (5, 3))
            self.canvas = FigureCanvas(self.figure)
            controls_layout.addWidget(self.canvas)
            self.take_images_button = QPushButton("Take Images")
            self.take_images_button.clicked.connect(self.take_images)
            controls_layout.addWidget(self.take_images_button)
            controls_group.setLayout(controls_layout)
            main_layout.addWidget(controls_group)
            self.setLayout(main_layout)
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
        
        
        def take_images(self):
            try:
                num_images = self.num_images_input.value()
                timeout = int(self.timeout_input.text())
                images = self.camera.take_images(num_images, timeout)
                self.image_data = images
                self.display_spectrum()
            except Exception as e:
                print(f"Error taking images: {e}")
        
        def set_directory(self):
            directory = QFileDialog.getExistingDirectory(self, "Select Directory")
            if directory:
                self.selected_directory = directory
                print(f"Selected directory: {self.selected_directory}")
        def display_spectrum(self):
            self.figure.clear()
            subplot = self.figure.add_subplot(111)
            
            if not self.image_data:
                print("No image data available to display.")
                return
            
            if len(self.image_data) == 1:
                image = self.image_data[0]
                if isinstance(image, (tuple, list)):
                    x, y = image
                
                else:
                    x = range(len(image))  # Assuming image is a 1D array
                    y = image
                x = [xi * 1e9 for xi in x]
                subplot.plot(x, y, label="Image 1")
            else:
                for i, image in enumerate(self.image_data):
                    if isinstance(image, (tuple, list)):
                        x, y = image
                    else:
                        x = range(len(image))
                        y = image
                    x = [xi * 1e9 for xi in x]
                    subplot.plot(x, y, label=f"Image {i+1}")
            subplot.set_xlabel("Wavelength (nm)")
            subplot.set_ylabel("Intensity")
            subplot.set_title("Spectral Data")
            subplot.legend()
            self.canvas.draw()

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
            # self.shamrock = Shamrock(name = "shamrock")
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