import sys
import logging
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QFormLayout, QLineEdit, QComboBox, QHBoxLayout
from PyQt5.QtCore import QTimer
from bluesky import RunEngine
from bluesky.plans import count
from bluesky.callbacks import LiveTable
from ophyd import Signal
from ophyd.sim import motor
from pybridge.MoveBridge.sbisBridge import SBISMoveBridge

# Setup Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class InstrumentController(QWidget):
    def __init__(self, instrument_name="instrument"):
        super().__init__()

        self.setWindowTitle(f"{instrument_name} Control Panel")
        self.instrument = SBISMoveBridge(name="sbis", driver="ASRL4::INSTR")

        self.initUI()
        self.re = RunEngine({})
        self.re.subscribe(LiveTable([self.instrument]))

    def initUI(self):
        layout = QVBoxLayout()
        self.status_label = QLabel("Status: Idle")
        layout.addWidget(self.status_label)

        # Create form layout for settings
        self.form_layout = QFormLayout()
        self.param_widgets = {}
        self.param_inputs = {}  # Store input widgets for parameter modification

        # Dynamically detect parameters and add to GUI
        for attr in dir(self.instrument):
            try:
                if isinstance(getattr(self.instrument, attr), Signal):
                    # Create horizontal layout for each parameter
                    param_layout = QHBoxLayout()
                    
                    # Value display label
                    value_label = QLabel("^-^") # (^_-)/\(^_^) <(~_~) zzZZZ   
                    self.param_widgets[attr] = value_label
                    param_layout.addWidget(value_label)
                    
                    # Input field for manual entry
                    input_field = QLineEdit()
                    input_field.setPlaceholderText("Enter value...")
                    input_field.returnPressed.connect(lambda checked, a=attr, field=input_field: self.update_parameter(a, field.text()))
                    self.param_inputs[attr] = input_field
                    param_layout.addWidget(input_field)
                    
                    # Update button
                    update_btn = QPushButton("Set")
                    update_btn.clicked.connect(lambda checked, a=attr, field=input_field: self.update_parameter(a, field.text()))
                    param_layout.addWidget(update_btn)
                    
                    # Create container widget for the layout
                    param_widget = QWidget()
                    param_widget.setLayout(param_layout)
                    
                    self.form_layout.addRow(QLabel(attr), param_widget)
            except:
                continue

        layout.addLayout(self.form_layout)

        # Buttons
        self.start_button = QPushButton("Start Measurement")
        self.start_button.clicked.connect(self.start_measurement)
        layout.addWidget(self.start_button)

        self.setLayout(layout)

        # Timer for live updates
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_values)
        self.timer.start(1000)  # Update every second

    def update_values(self):
        """Fetch latest readings from the instrument and update UI."""
        for attr, widget in self.param_widgets.items():
            try:
                value = getattr(self.instrument, attr).get()
                widget.setText(str(value))
            except Exception as e:
                logger.error(f"Error reading {attr}: {e}")
                widget.setText("Error")
    
    def click_button(self, param_name, value):
        """Handle button click event."""
        try:
            attr = getattr(self.instrument, param_name)
            widget = self.param_widgets.get(param_name)
            value = attr.get()
            widget.setText(str(value))
        except Exception as e:
            logger.error(f"Error accessing {param_name}: {e}")
            return
        

    def start_measurement(self):
        """Run a measurement using Bluesky."""
        self.status_label.setText("Status: Running")
        try:
            self.re(count([self.instrument], num=1))
        except Exception as e:
            self.status_label.setText("Status: Error")
            logger.error(f"Error running measurement: {e}")
        else:
            self.status_label.setText("Status: Idle")
    
    def update_parameter(self, param_name, value):
        try:
            attribute = getattr(self.instrument, param_name)
            if isinstance(attribute, Signal):
                try:
                    numeric_value = float(value)
                    if numeric_value.is_integer():
                        numeric_value = int(numeric_value)
                except ValueError:
                    numeric_value = value
                
                try:
                    old_value = attribute.get()
                    print(f"Before update: {param_name} = {old_value}")
                except Exception as e:
                    print(f"Error fetching old value for {param_name}: {e}")
                    old_value = "Unknown"
                
                print(f"Setting {param_name} to {numeric_value}")
                
                if hasattr(attribute, 'limits'):
                    print(f"{param_name} limits: {attribute.limits}")
                if hasattr(attribute, 'check_value'):
                    try:
                        attribute.check_value(numeric_value)
                        print(f"Value {numeric_value} passed validation")
                    except Exception as e:
                        print(f"Value {numeric_value} failed validation: {e}")
                        self.status_label.setText(f"Invalid value for {param_name}: {e}")
                        return
                
                try:
                    put_result = attribute.put(numeric_value)
                    print(f"Put operation result: {put_result}")
                    
                    if hasattr(put_result, 'success'):
                        print(f"Put success: {put_result.success}")
                    if hasattr(put_result, 'done'):
                        print(f"Put done: {put_result.done}")
                        
                except Exception as e:
                    print(f"Error during put operation: {e}")
                    self.status_label.setText(f"Put failed for {param_name}: {e}")
                    return
                

                def check_final_value():
                    try:
                        actual_value = attribute.get()
                        print(f"After update: {param_name} = {actual_value}")
                        
                        widget = self.param_widgets.get(param_name)
                        if widget:
                            widget.setText(str(actual_value))
                        
                        if str(actual_value) == str(old_value):
                            self.status_label.setText(f"WARNING: {param_name} did not change! Still {actual_value}")
                            print(f"WARNING: {param_name} value unchanged - instrument may have rejected the command")
                        else:
                            self.status_label.setText(f"{param_name} updated: {old_value} → {actual_value}")
                        
                            input_field = self.param_inputs.get(param_name)
                            if input_field:
                                input_field.clear()
                                
                    except Exception as e:
                        self.status_label.setText(f"Error reading {param_name}: {e}")
                        print(f"Error fetching final value for {param_name}: {e}")
                

                QTimer.singleShot(300, check_final_value)
                    
            else:
                logger.error(f"{param_name} is not a Signal.")
        except Exception as e:
            self.status_label.setText(f"Error updating {param_name}: {e}")
            logger.error(f"Error updating {param_name}: {e}")
    

# Example Usage
if __name__ == "__main__": # Import your instrument class here

    app = QApplication(sys.argv)
    window = InstrumentController(instrument_name="SBIS")
    window.show()
    sys.exit(app.exec())
