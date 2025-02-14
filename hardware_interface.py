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
from ophyd import Device, Signal, PVPositioner, SignalRO
from ophyd.sim import NullStatus, new_uid
from shrc203_VISADriver import SHRC203VISADriver as SHRC

logger = logging.getLogger(__name__)


class SHRCStage(PVPositioner):
    # DK - or PVPositioner, which one is better?
    axis_component = Cpt(Signal, value=1)
    speed_ini = Cpt(Signal, value=10000)
    speed_fin = Cpt(Signal, value=10000)
    accel_t = Cpt(Signal, value=100)
    setpoint = Cpt(SignalRO, value=0.0)
    loop = Cpt(Signal, value=0)
    unit = Cpt(Signal, value="um")
    # DK add done and done_value property

    params = {
        "visa_name": {
            "title": "Instrument Address:",
            "type": "str",
            "value": "ASRL3::INSTR",
        },
        "unit": {
            "title": "Unit:",
            "limits": ["um", "mm", "nm", "deg", "pulse"],
            "value": "um",
        },
        "loop": {"title": "Loop:", "value": 0},
        "speed_ini": {"title": "Speed Initial:", "type": "float", "value": 0},
        "accel_t": {"title": "Acceleration Time:", "type": "float", "value": 1},
        "speed_fin": {"title": "Speed Final:", "type": "float", "value": 1.2},
        "axis": {
            "title": "Axis",
            "type": "list",
            "limits": ["X", "Y", "Z"],
            "value": "X",
        },
    }
    axis_int = {"X": 1, "Y": 2, "Z": 3}

    def __init__(
        self,
        prefix="",
        *,
        limits=True,
        name=None,
        read_attrs=None,
        configuration_attrs=None,
        parent=None,
        egu=" ",
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
        # super().__init__(
        #     prefix=prefix,
        #     name=name,
        #     kind=kind,
        #     read_attrs=read_attrs,
        #     configuration_attrs=configuration_attrs,
        #     parent=parent,
        #     **kwargs,
        # )
        
        self.stage = SHRC(self.params["visa_name"]["value"])
        self.stage.open_connection()
        self.stage.set_unit(self.params["unit"]["value"])
        self.axis_component.put(self.axis_int[self.params["axis"]["value"]])
        self._egu = self.params['unit']['value']
        self.done = False
        # self.setpoint = self.stage.get_position(self.axis_component.get())

    def set_axis(self, axis):
        if axis in self.axis_int:
            self.axis_component.put(axis.value)
        else:
            self.axis_component.put(axis.value)
            logger.warning("Invalid axis. Defaulting to axis X")

    def get_axis(self):
        return self.axis_component.get()

    def commit_settings(self):
        if (
            self.params["speed_ini"]
            and self.params["speed_fin"]
            and self.params["accel_t"] is not None
        ):
            self.speed_ini.put(self.params["speed_ini"]["value"])
            self.speed_fin.put(self.params["speed_fin"]["value"])
            self.accel_t.put(self.params["accel_t"]["value"])
            self.stage.set_speed(
                self.params["speed_ini"]["value"],
                self.params["speed_fin"],
                self.params["accel_t"],
                self.axis_component.get(),
            )

        elif self.params["unit"] is not None:
            self.unit.put(self.params["unit"])
            self.stage.set_unit(self.params["unit"])

        elif self.params["loop"] is not None:
            self.loop.put(self.params["loop"])
            self.stage.set_loop(self.params["loop"])

    def move(self, position: float, wait=True, timeout=None):
        self.stage.move(position, self.axis_component.get())
        self.done = self.stage.get_done()

        # if self.get_position() == position:
        #     logger.info(f"Stage moved to position {position}")
        # else:
        #     logger.error(f"Stage failed to move to position {position}")
        # return MoveStatus(positioner = self, target = position, done=True, success=True)

        # DK - Should we update the class properties?
        # DK - the original method returns a MoveStatus object. How can we implement this?

    def move_relative(self, position, wait=True, timeout=None):
        # DK - self.axis is a list. Is self.axis.value valid?
        self.stage.move_relative(position, self.axis_component.get())
        if self.get_position() == position:
            logger.info(f"Stage moved to position {position}")
        else:
            logger.error(f"Stage failed to move to position {position}")
        
        self.done = self.stage.get_done()

    def home(self, wait=True, timeout=None):
        self.stage.home(self.axis_component.get())
        self.done = self.stage.get_done()
        return MoveStatus(positioner=self, target=0, done=True, success=True)

    @property
    def get_position(self):  # DK - compare with the original position method
        """Return the current position of the stage.

        Returns
        -------
         int: The current position of the stage.
        """
        position = self.stage.get_position(self.axis_component.get())
        self.setpoint = position  # TypeError: 'int' object is not callable
        return position

    def stop(self, *, success: bool = False):
        self.stage.stop(self.axis_component.get())
        # self._done_moving(success=success)

    def close_connection(self):
        self.stage.close()


# For PYQT5, we need to load widgets and text to have the commit_settings to load in the GUI
