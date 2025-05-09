# Thorlabs.MotionControl.KCube.Solenoid.dll
# Thorlabs.MotionControl.KCube.SolenoidCLI.dll

import clr 
import sys
import logging 
logger = logging.getLogger(__name__)
import os


ksc_path = "C:\\Program Files\\Thorlabs\\Kinesis"
sys.path.append(ksc_path)

clr.AddReference("Thorlabs.MotionControl.KCube.SolenoidCLI")
clr.AddReference("Thorlabs.MotionControl.DeviceManagerCLI")


import Thorlabs.MotionControl.KCube.SolenoidCLI as Solenoid
import Thorlabs.MotionControl.DeviceManagerCLI as Device

Device.DeviceManagerCLI.BuildDeviceList()

serial_numbers = [str(ser) for ser in Device.DeviceManagerCLI.GetDeviceList(Solenoid.KCubeSolenoid.DevicePrefix)]

class KSC101:
    def __init__(self):
        self._solenoid = None
    
    def connect(self):
        self._solenoid = (Solenoid.KCubeSolenoid.CreateKCubeSolenoid(serial_numbers[0]))
        self._solenoid.Connect(serial_numbers[0]) 
        self._solenoid.WaitForSettingsInitialized(5000)
        self._solenoid.StartPolling(100) 
        self._solenoid.EnableDevice()
    
    def set_state(self, state):
        pass 

    # def get_cycle(self):
    #     return self._solenoid.Cycle()
    
    def set_operating_mode(self, mode):
        if mode == "Manual":
            self._solenoid.
    
    def set_rotation(self):
        self._solenoid.TriggerRotation()

    def disconnect(self):
        self._solenoid.Disconnect()

