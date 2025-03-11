import datetime
import itertools
import os
import warnings
from collections import deque
from pathlib import Path
import logging
from pyvisa.errors import VisaIOError as VISAError

# import h5py
import numpy as np
from enum import Enum
from pandas import DataFrame
import pandas as pd
from ophyd.status import MoveStatus
from event_model import compose_resource
from ophyd import Component as Cpt
from ophyd import Device, Signal, PVPositioner, SignalRO
from ophyd.status import MoveStatus, StatusBase
from ophyd.sim import NullStatus, new_uid
from csv_convert_parent import csv_convert_parent
from hardware_bridge.shrc203_VISADriver import SHRC203VISADriver as SHRC

# logger = logging.getLogger(__name__)
from ophyd.log import config_ophyd_logging
config_ophyd_logging()
logger = logging.getLogger(__name__)


class SHRCStage(PVPositioner):
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

        self.shrc = SHRC(self.params["visa_name"]["value"])
        try: 
            self.shrc.open_connection()
            self.shrc.set_unit(self.params["unit"]["value"])
            self.axis_component.put(self.axis_int[self.params["axis"]["value"]])
            self._egu = self.params['unit']['value']
        except VISAError as e:
            logger.error(f"Failed to connect to the instrument: {e}")
            self.close()
            self.reconnect()

        # self.done.get = self.shrc.wait_for_ready
        # self.stop_signal.put = self.shrc.stop
        # self.setpoint = self.shrc.get_position(self.axis_component.get())
    def reconnect(self):
        try: 
            self.shrc.open_connection()
            self.shrc.set_unit(self.params["unit"]["value"])
            self.axis_component.put(self.axis_int[self.params["axis"]["value"]])
            self._egu = self.params['unit']['value']
            logger.info("Reconnected to the Instrument")
        except VISAError as e:
            logger.error(f"Failed to connect to the instrument: {e}")
            self.close()

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
            self.shrc.set_speed(
                self.params["speed_ini"]["value"],
                self.params["speed_fin"]['value'],
                self.params["accel_t"]["value"],
                self.axis_component.get(),
            )

        elif self.params["unit"] is not None:
            self.unit.put(self.params["unit"])
            self.shrc.set_unit(self.params["unit"])

        elif self.params["loop"] is not None:
            self.loop.put(self.params["loop"])
            self.shrc.set_loop(self.params["loop"])

    
    def move(self, position: float, moved_cb=None, wait=True, timeout=None):
        self.setpoint.put(position)
        value = self.shrc.move(self.setpoint.get(), self.axis_component.get())
        print(value)
        status = MoveStatus(self, target = position, timeout = timeout,
                            # settle_time = self._settle_time
                            )
        if value == 1: 
            self.done.put(value = True) #shrc successfully moved
            print("done true")
        else: 
            self.done.put(value = False)
            print("done false")
        status.set_finished()
        # has_done = self.done is not None
        # if not has_done:
        #     moving_vals = 1 - self.done_value
        #     self._move_changed(value=self.done_value)
        #     self._move_changed(value=moving_vals)
        return status
    
    def get_position(self): 
        return self.shrc.query_position(self.axis_component.get())
    
    def home(self):
        self.shrc.home(self.axis_component.get())
        self.setpoint.put(self.get_position())
        logger.debug("Actuators have moved home")
        
    def move_relative(self, position):
        
        target_position = self.readback.get() + position
        self.setpoint.put(target_position) #Set the increment
        # position = self.target_position - self.get_position()

        self.shrc.move_relative(target_position, self.axis_component.get())

    def close(self):
        self.shrc.__del__()

        # if self.get_position() == position:
        #     logger.info(f"shrc moved to position {position}")
        # else:
        #     logger.error(f"shrc failed to move to position {position}")
        # return MoveStatus(positioner = self, target = position, done=True, success=True)

        # DK - Should we update the class properties?
        # DK - the original method returns a MoveStatus object. How can we implement this?

    # def move_relative(self, position, wait=True, timeout=None):
    #     # DK - self.axis is a list. Is self.axis.value valid?
    #     self.shrc.move_relative(position, self.axis_component.get())
    #     if self.get_position() == position:
    #         logger.info(f"shrc moved to position {position}")
    #     else:
    #         logger.error(f"shrc failed to move to position {position}")
        
    #     self.done = self.shrc.get_done()

    # def home(self, wait=True, timeout=None):
    #     self.shrc.home(self.axis_component.get())
    #     self.done = self.shrc.get_done()
    #     return MoveStatus(positioner=self, target=0, done=True, success=True)

    # @property
    # def get_position(self):  # DK - compare with the original position method
    #     """Return the current position of the shrc.

    #     Returns
    #     -------
    #      int: The current position of the shrc.
    #     """
    #     position = self.shrc.get_position(self.axis_component.get())
    #     self.setpoint = position  # TypeError: 'int' object is not callable
    #     return position

    def stop(self, *, success: bool = False):
        if self.stop_signal is not None:
            self.stop_signal.put(value = self.stop_value)        
        self.shrc.stop(self.axis_component.get())
    
    def save_csv(self, data):
        df = pd.DataFrame(data)
        export_path = Path("data6_excel")
        export_path.mkdir(parents = True, exist_ok = True)
        filename = export_path / "test.xlsx"

        # with pd.ExcelWriter(filename, engine="xlsxwriter") as writer:
        #     df.to_excel(writer, sheet_name="data", index=False)
        # df.to_csv(filename, index = False)

        # parent_filename = export_path / "parent.csv"
        # filename = parent_filename
        # tab_name = f"NewTab_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
        # # csv_convert_parent(filename, parent_filename, tab_name)

        # df.to_excel(filename, sheet_name=tab_name, index=False)
        # super().stop(success=success)
        # self._done_moving(success=success)

    # def close_connection(self):
    #     self.shrc.close() 



# For PYQT5, we need to load widgets and text to have the commit_settings to load in the GUI
if __name__ == "__main__":
    from MoveBridge.hardware_interface import SHRCStage
    from bluesky import RunEngine
    from bluesky.callbacks.best_effort import BestEffortCallback
    from bluesky.utils import ProgressBarManager
    from bluesky.plans import count
    from bluesky.callbacks import LiveTable, LivePlot
    from ophyd.sim import motor, det
    from bluesky.plans import scan
    import matplotlib.pyplot as plt
    import h5py
    from ophyd.sim import det1, det2

    plt.ion()
    shrc203 = SHRCStage(name="shrc203")

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
    RE(scan([shrc203], motor, -1, 1, 10))

    # RE(scan([det], shrc203, 1, 3, 10))

    header = db[-1]
    df = header.table()
    metadata = header.start

    # data = metadata.values()
    data = header.documents()

    # # df.to_hdf("data.h5", key = "df", mode = "w")
    # with h5py.File("data_with.h5", "w") as f:
    #     # set = f.create_dataset("mydataset", (100,), dtype = "i")
    #     for key, value in metadata.items():
    #         f.attrs[key] = str(value)
    #         # f.attrs[key] = df[value]
    #         # df[key] = value
    # df.to_hdf("data_with.h5", key = "df", mode = "w", format = "table")
            
    # from suitcase import pybridge
    from suitcase import nano_pybridge, csv
    nano_pybridge.export(gen=data, directory="data7")
    shrc203.save_csv(df)
    # export_path = Path("data4_csv")
    # csv.export(data, "data4_csv")
    # df = pd.DataFrame(data)
    # export_path = Path("data4_csv")
    # export_path.mkdir(parents = True, exist_ok = True)
    # filename = export_path / "test.csv"
    # df.to_csv(filename, index = False)
    # # filename = os.path.join(export_path, "test.csv")
    # parent_filename = "parent.csv"
    # tab_name = "NewTab"
    # csv_convert_parent(filename, parent_filename, tab_name)
    print("Data saved to data3_csv")


    # print("Data saved to data.h5")
    # plt.show(block = True)


    # dets = [keithley]
    # RE(one_run_one_event(dets))

    # print(f"keithley.read(): {keithley.read()}")
    # print(f"keithley.get(): {keithley.get()}")
    # print(f"keithley.voltage: {keithley.voltage.get()}")
    plt.show()
    