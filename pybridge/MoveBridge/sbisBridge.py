from pathlib import Path
import logging
from pyvisa.errors import VisaIOError as VISAError
import pandas as pd
from ophyd import Component as Cpt
from ophyd import Signal, Device, PVPositioner, SignalRO
from ophyd.status import MoveStatus
from pybridge.csv_convert_parent import csv_convert_parent
from pybridge.hardware_bridge.sbis26_VISADriver import SBIS26VISADriver
 
class SBISMoveBridge(PVPositioner):
    setpoint = Cpt(Signal) #target position
    readback = Cpt(SignalRO) #Read position
    done = Cpt(Signal, value = False) #Instrument is done moving
    actuate = Cpt(Signal) #Request to move
    stop_signal =  Cpt(Signal) #Request to stop
 
    axis_component = Cpt(Signal, value=1, kind="config")
    speed_ini = Cpt(Signal, value=2000, kind="config")
    speed_fin = Cpt(Signal, value=20000, kind="config")
    accel_t = Cpt(Signal, value=100, kind="config")
    # store_position = Cpt(Signal, value=0.0, kind="hinted")
    loop = Cpt(Signal, value=0, kind="config")
    unit = Cpt(Signal, value="um", kind="config")
    # DK add done and done_value property
 
    def __init__(
        self,
        prefix="",
        *,
        limits=None,
        name=None,
        read_attrs=None,
        configuration_attrs=None,
        parent=None,
        egu="",
        driver = None,
        **kwargs,
    ):
        super().__init__(
            prefix=prefix,
            read_attrs=read_attrs,
            configuration_attrs=configuration_attrs,
            name=name,
            parent=parent,
            **kwargs,
        )
        if isinstance(driver, SBIS26VISADriver):
            self.sbis = driver
        elif driver is not None:
            self.sbis = SBIS26VISADriver(driver)
        else:
            raise ValueError("Not correct connection to SBIS")

        self.readback.get = self.get_position
        self.setpoint.put = self.move
 
    def get_position(self):
        """Get the current position of the stage."""
        return self.sbis.get_position(self.axis_component.get())
   
    def move(self, position: float, wait=True, timeout=None):
        value = self.sbis.move(position, self.axis_component.get())
        print(value)
        status = MoveStatus(self, target = position, timeout = timeout, settle_time = self._settle_time)
        if value == 1:
            self.done.put(value = True) #shrc successfully moved
            print("done true")
        else:
            self.done.put(value = False)
            print("done false")
        status.set_finished()
        return status

    def home(self):
        """Home the stage."""
        self.sbis.home(self.axis_component.get())
        self.done.put(value = True)
   
    def stop(self):
        """Stop the stage."""
        self.sbis.stop()
        self.done.put(value = False)
        # self.setpoint.put(self.readback.get())
 
    def close(self):
        """Close the stage."""
        self.sbis.close()
        self.done.put(value = False)    

class SBISAxis(SBISMoveBridge):
    def __init__(
        self,
        prefix="",
        *,
        limits=None,
        name=None,
        read_attrs=None,
        configuration_attrs=None,
        parent=None,
        egu="",
        driver = None,
        axis = 1, 
        **kwargs,
    ):
        super().__init__(
            prefix=prefix,
            read_attrs=read_attrs,
            configuration_attrs=configuration_attrs,
            name=name,
            parent=parent,
            driver = driver,
            **kwargs,
        )
        self.sbis = driver
        self.axis = axis
 
    def move(self, position: float, wait=True, timeout=None):
        """Move the stage to the specified position."""
        value = self.sbis.move(position, self.axis)
        status = MoveStatus(self, target = position, timeout = timeout, settle_time = self._settle_time)
        if value == 1: 
            self.done.put(value = True)
        else:
            self.done.put(value = False)
        status.set_finished()
        return status

   
    def move_relative(self, position):
        """Move the stage to the relative """
        self.sbis.move_relative(position, self.axis) 

    def get_position(self):
        return self.sbis.get_position(self.axis)  
    def home(self):
        self.sbis.home(self.axis)   