# Thorlabs.MotionControl.KCube.Solenoid.dll
# Thorlabs.MotionControl.KCube.SolenoidCLI.dll

import clr 
import sys 

ksc_path = "C:\\Program Files\\Thorlabs\\Kinesis"
sys.path.append(ksc_path)

clr.AddReference("Thorlabs.MotionControl.KCube.SolenoidCLI")
clr.AddReference("Thorlabs.MotionControl.DeviceManagerCLI")


import Thorlabs.MotionControl.KCube.SolenoidCLI as Solenoid
import Thorlabs.MotionControl.DeviceManagerCLI as Device

Device.DeviceManagerCLU.BuildDeviceList()

serial_numbers = [str(ser) for ser in Device.DeviceManagerCLI.GetDeviceList(Solenoid.DevicePrefix)]

