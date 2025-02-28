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
from hardware_bridge.shrc203_VISADriver import SHRC203VISADriver as SHRC

logger = logging.getLogger(__name__)


class SHRCStage(PVPositioner):
    setpoint = Cpt(Signal) #target position
    readback = Cpt(SignalRO) #Read position
    done = Cpt(SignalRO, value = False) #Instrument is done moving
    actuate = Cpt(Signal) #Request to move
    stop_signal =  Cpt(Signal) #Request to stop

    axis_component = Cpt(Signal, value=1)
    speed_ini = Cpt(Signal, value=2000)
    speed_fin = Cpt(Signal, value=20000)
    accel_t = Cpt(Signal, value=100)
    # store_position = Cpt(Signal, value=0.0, kind="hinted")
    loop = Cpt(Signal, value=0)
    unit = Cpt(Signal, value="um")
    # DK add done and done_value property

    params = {
        "visa_name": {
            "title": "Instrument Address:",
            "type": "valuestr",
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
        limits=None,
        name=None,
        read_attrs=None,
        configuration_attrs=None,
        parent=None,
        egu="",
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

        self.readback.get = self.get_position
        self.stage = SHRC(self.params["visa_name"]["value"])
        self.stage.open_connection()
        self.stage.set_unit(self.params["unit"]["value"])
        self.axis_component.put(self.axis_int[self.params["axis"]["value"]])
        self._egu = self.params['unit']['value']
        # self.done.get = self.stage.wait_for_ready
        # self.stop_signal.put = self.stage.stop
        # self.setpoint = self.stage.get_position(self.axis_component.get())

    def set_axis(self, axis):
        if axis in self.axis_int.values():
            self.axis_component.put(axis)
        else:
            self.axis_component.put(1)
            logger.warning("Invalid axis. Defaulting to axis X")

    # def get_axis(self):
    #     return self.axis_component.get()

    def commit_settings(self):
        # Incorporate shrc.speed_ini.put(...)
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
                self.params["speed_fin"]['value'],
                self.params["accel_t"]["value"],
                self.axis_component.get(),
            )

        elif self.params["unit"] is not None:
            self.unit.put(self.params["unit"])
            self.stage.set_unit(self.params["unit"])

        elif self.params["loop"] is not None:
            self.loop.put(self.params["loop"])
            self.stage.set_loop(self.params["loop"])

    # def move(self, position: float, wait=True, timeout=None):
    #     self.stage.move(position, self.axis_component.get())
    #     self.done = self.stage.get_done()
    #     done = MoveStatus(positioner= self, target=position)
    #     return done
    
    def move_absolute(self, position: float, wait=True, timeout=None):
        self.setpoint.put(position)
        # self.actuate.put(1)
        self.stage.move(self.setpoint.get(), self.axis_component.get())
    
    def get_position(self): 
        return self.stage.query_position(self.axis_component.get())
    
    def home(self):
        self.stage.home(self.axis_component.get())
        self.setpoint.put(self.get_position())
        logger.debug("Actuators have moved home")
        
    def move_relative(self, position):
        
        target_position = self.readback.get() + position
        self.setpoint.put(target_position) #Set the increment
        # position = self.target_position - self.get_position()
 
        self.stage.move_relative(target_position, self.axis_component.get())
 
    def close(self):
       self.stage.close()
 
         # if self.get_position() == position:
        #     logger.info(f"Stage moved to position {position}")
        # else:
        #     logger.error(f"Stage failed to move to position {position}")
        # return MoveStatus(positioner = self, target = position, done=True, success=True)

        # DK - Should we update the class properties?
        # DK - the original method returns a MoveStatus object. How can we implement this?

    # def move_relative(self, position, wait=True, timeout=None):
    #     # DK - self.axis is a list. Is self.axis.value valid?
    #     self.stage.move_relative(position, self.axis_component.get())
    #     if self.get_position() == position:
    #         logger.info(f"Stage moved to position {position}")
    #     else:
    #         logger.error(f"Stage failed to move to position {position}")
        
    #     self.done = self.stage.get_done()

    # def home(self, wait=True, timeout=None):
    #     self.stage.home(self.axis_component.get())
    #     self.done = self.stage.get_done()
    #     return MoveStatus(positioner=self, target=0, done=True, success=True)

    # @property
    # def get_position(self):  # DK - compare with the original position method
    #     """Return the current position of the stage.

    #     Returns
    #     -------
    #      int: The current position of the stage.
    #     """
    #     position = self.stage.get_position(self.axis_component.get())
    #     self.setpoint = position  # TypeError: 'int' object is not callable
    #     return position

    # def stop(self, *, success: bool = False):
    #     self.stage.stop(self.axis_component.get())
    #     # self._done_moving(success=success)

    # def close_connection(self):
    #     self.stage.close()


# For PYQT5, we need to load widgets and text to have the commit_settings to load in the GUI
if __name__ == "__main__":
    from MoveBridge.hardware_interface import SHRCStage
    from bluesky import RunEngine
    from bluesky.callbacks.best_effort import BestEffortCallback
    from bluesky.utils import ProgressBarManager
    from bluesky.plans import count
    from bluesky.callbacks import LiveTable, LivePlot
    from ophyd.sim import motor
    from bluesky.plans import scan
    import matplotlib.pyplot as plt
    import h5py

    plt.ion()
    shrc = SHRCStage(name="shrc203")

    RE = RunEngine({})
    bec = BestEffortCallback()
    RE.subscribe(bec)
    RE.waiting_hook = ProgressBarManager()

    from databroker import Broker
    db = Broker.named("temp")
    
    RE.subscribe(db.insert)
    # live_plot = LivePlot('keithley_voltage', 'motor')
    # RE.subscribe(live_plot)

    # token = RE.subscribe(LiveTable([keithley]))
    # RE(count([keithley], num=5, delay=0.1))
    RE(scan([shrc], motor, -1, 1, 10))

    header = db[-1]
    df = header.table()

    # header = db[-1]
    # df = header.table()
    metadata = header.start

    df.to_hdf("data.h5", key = "df", mode = "w")
    # with h5py.File("data_with.h5", "a") as f:
    #     for key, value in metadata.items():
    #         f.attrs[key] = value
    
    print("Data saved to data.h5")
    # plt.show(block = True)


    # dets = [keithley]
    # RE(one_run_one_event(dets))

    # print(f"keithley.read(): {keithley.read()}")
    # print(f"keithley.get(): {keithley.get()}")
    # print(f"keithley.voltage: {keithley.voltage.get()}")
    plt.show()
    