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
from ophyd.status import MoveStatus
from event_model import compose_resource
from ophyd import Component as Cpt
from ophyd import Device, Signal, PVPositioner
from ophyd.sim import NullStatus, new_uid
from shrc203_VISADriver import SHRC203VISADriver as SHRC

from nomad_camels.bluesky_handling.custom_function_signal import (
    Custom_Function_Signal,
    Custom_Function_SignalRO,
)
from nomad_camels.bluesky_handling.custom_function_signal import Custom_Function_Signal


logger = logging.getLogger(__name__)

class Axis(Enum): 
    X = 1
    Y = 2 
    Z = 3

class SHRCStage(PVPositioner):
    # DK - or PVPositioner, which one is better?
    axis_component = Cpt(Custom_Function_Signal, name = 'axis_component', value = Axis.X.value)
    speed_ini = Cpt(Custom_Function_Signal, name = 'speed_ini', value = 10000)
    speed_fin = Cpt(Custom_Function_Signal, name = 'speed_fin', value = 10000)
    accel_t = Cpt(Custom_Function_Signal, name = 'accel_t', value = 100)
    get_position = Cpt(Custom_Function_SignalRO, name = 'get_position', value = 0.0)
    loop = Cpt(Custom_Function_Signal, name = 'loop', value = 0)
    unit = Cpt(Custom_Function_Signal, name = 'unit', value = 'um')

    params = [
        {"title": "Instrument Address:","name": "visa_name","type": "str","value": "ASRL3::INSTR",},
        {"title": "Unit:", "name": "unit", "type": "list", "limits": ["um", "mm", "nm", "deg", "pulse"],"value": "um",},
        {"title": "Loop:", "name": "loop", "type": "int", "value": 0},
        {"title": "Speed Initial:", "name": "speed_ini", "type": "float", "value": 0},
        {"title": "Acceleration Time:", "name": "accel_t", "type": "float", "value": 1},
        {"title": "Speed Final:", "name": "speed_fin", "type": "float", "value": 1.2},
    ]



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
        self.stage.set_position(self.position, Axis.X.value)
        self.stage.set_velocity(self.speed_initial.get(), Axis.X.value)
        self.stage.set_acceleration(self.accel_initial.get(), Axis.X.value) 

            
    def move(self, position: float, wait = True, timeout = None):
        # DK - self.axis is a list. Is self.axis.value valid?
        self.stage.move(position, Axis.X.value)
        return MoveStatus(positioner = self, target = position, done=True, success=True)
        
        # DK - Should we update the class properties?
        # DK - the original method returns a MoveStatus object. How can we implement this?
    
    def move_relative(self, position, wait = True, timeout = None):
        # DK - self.axis is a list. Is self.axis.value valid?
        self.stage.move_relative(position, Axis.X.value)
    
    def home(self, wait = True, timeout = None):
        self.stage.home(Axis.X.value)
        return MoveStatus(positioner = self, target = 0, done=True, success=True)
    
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
    
    def close_connection(self):
        self.stage.close_connection()
