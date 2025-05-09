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
    def __init__(self, serial='68800739'):
        self._solenoid = None
        self.serial = serial
    
    def connect(self):
        if self.serial in serial_numbers:
            self._solenoid = (Solenoid.KCubeSolenoid.CreateKCubeSolenoid(self.serial))
            self._solenoid.Connect(serial_numbers[0]) 
            self._solenoid.WaitForSettingsInitialized(5000)
            self._solenoid.StartPolling(100) 
            self._solenoid.EnableDevice()
            self._solenoid.GetSolenoidConfiguration(self.serial)
            self._solenoid.SetOperatingMode(Solenoid.SolenoidStatus.OperatingModes.Manual)
        
        else:
            raise ConnectionError("KSC101 not connected. Serial Number input is not in list")
     
    def set_rotation(self):
        self._solenoid.TriggerRotation()

    def get_shutter_state(self):
        value = self._solenoid.GetOperatingState()
        value = value.value__
        if value == 1:
            return "Active"
        elif value == 2:
            return "Inactive"
        else:
            raise ValueError("Value is unknown. Check again if Device is connected")
    
    def open_shutter(self):
        self._solenoid.SetOperatingState(Solenoid.SolenoidStatus.OperatingStates.Active)
    
    def close_shutter(self):
        self._solenoid.SetOperatingState(Solenoid.SolenoidStatus.OperatingStates.Inactive)

    def disconnect(self):
        self._solenoid.StopPolling()
        self._solenoid.Disconnect()
    


