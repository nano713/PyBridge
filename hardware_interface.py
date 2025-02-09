import datetime
import itertools
import os
import warnings
from collections import deque
from pathlib import Path
import logging

import h5py
import numpy as np
from enum import Enum
from .status import MoveStatus
from event_model import compose_resource
from ophyd import Component as Cpt
from ophyd import Device, Signal, PVPositioner
from ophyd.sim import NullStatus, new_uid
from shrc203_VISADriver import SHRC203VISADriver as SHRC

logger = logging.getLogger(__name__)

class Axis(Enum): 
    X = 1
    Y = 2 
    Z = 3

class SHRCStage(PVPositioner):
    # DK - or PVPositioner, which one is better?
    axis_component = Cpt(Signal, value = Axis.X.value)
    speed_initial = Cpt(Signal, value = 1.0)
    accel_initial = Cpt(Signal, value = 1.0)
    position_initial = Cpt(Signal, value = 0.0)
    
    # params = [{axis_component, speed_initial, accel_initial, position_initial}]
    # # {"key": value, "key": value, "key": value}

    def __init__(self, com, name: str, settle_time, egu = ' '): 
        self.stage = SHRC(com)
        self.stage.open_connection()
        self._position = self.stage.get_position(self.axis_component.get())
        # self.name = name
        # self.settle_time = settle_time
        self._egu = egu
        
     
    def set_axis(self, axis: Axis): 
        if axis in Axis:
            self.axis_component.put(axis.value)
        else: 
            self.axis_component.put(Axis.X.value)
            logger.warning("Invalid axis. Defaulting to axis X")
    
    def get_axis(self): 
        return self.axis_component.get()
    
    def commit_settings(self):
        self.stage.set_position(self.position, self.axis_component.get())
        self.stage.set_velocity(self.speed_initial.get(), self.axis_component.get())
        self.stage.set_acceleration(self.accel_initial.get(), self.axis_component.get()) 

            
    def move(self, position: float, wait = True, timeout = None):
        # DK - self.axis is a list. Is self.axis.value valid?
        self.stage.move(position, self.axis_component.get())
        return MoveStatus(positioner = self, target = position, done=True, success=True)
        
        # DK - Should we update the class properties?
        # DK - the original method returns a MoveStatus object. How can we implement this?
    
    def move_relative(self, position, wait = True, timeout = None):
        # DK - self.axis is a list. Is self.axis.value valid?
        self.stage.move_relative(position, self.axis_component.get())
    
    @property
    def position(self): # DK - compare with the original position method
        """Return the current position of the stage.  

           Returns
           -------
            int: The current position of the stage.
        """
        self._position = self.stage.get_position(self.axis.value) 
        return self._position
    
    def stop(self, *, success: bool = False):
        self.stage.stop(self.axis_component.get())
        self._done_moving(success=success)
