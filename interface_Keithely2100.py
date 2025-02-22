import logging

from ophyd import Device, Component as Cpt, Signal, SignalRO
# from pymeasure.instruments.keithley.keithley2000 import Keithley2000 
from keithley2100_VISADriver import Keithley2100VISADriver as Keithley
import threading
import time
# #Keithley2000 works for Keithley2100
# import pyvisa

logger = logging.getLogger(__name__)

class Keithley2100(Device):

    voltage = Cpt(SignalRO, kind="hinted")
    mode = Cpt(Signal, value="VOLT:DC", kind="config")

    params = {
        "resources": {
            "title": "Resources",
            "name": "resources",
            "type": "str",
            "value": "USB0::0x05E6::0x2100::1149087::INSTR",
        },
        "K2100Params": {
            "title": "Keithley2100 Parameters",
            "name": "K2100Params",
            "type": "group",
            "children": [
                {"title": "ID", "name": "ID", "type": "text", "value": ""},
                {
                    "title": "Mode",
                    "name": "mode",
                    "type": "list",
                    "limits": ["VOLT:DC", "VOLT:AC", "RES", "FRES", "CURR:DC", "CURR:AC"],
                    # ValueError: Value of voltage` is not in the discrete set {'current': 'CURR:DC', 'current ac': 'CURR:AC', 'voltage': 'VOLT:DC', 'voltage ac': 'VOLT:AC', 'resistance': 'RES', 'resistance 4W': 'FRES', 'period': 'PER', 'frequency': 'FREQ', 'temperature': 'TEMP', 'diode': 'DIOD', 'continuity': 'CONT'}
                    "value": "VOLT:DC",
                },
            ],
        },
    }
    
    def __init__(
        self,
        prefix="",
        *,
        name,
        kind=None,
        read_attrs=None,
        configuration_attrs=None,
        parent=None,
        child_name_separator="_",
        **kwargs,
    ): 
        super().__init__(name=name, parent=parent, kind=kind, **kwargs)
        self._driver = Keithley(self.params["resources"]["value"])
        self._driver.init_hardware()
        # self.voltage.get(self._driver.voltage)
        # self.voltage.get = lambda: self._driver.read()
        self.voltage.get = lambda: self.measure()

        mode_string = next((item for item in self.params["K2100Params"]["children"] if item["name"] == "mode"))
        self.mode.put(mode_string["value"])
        self._driver.set_mode(self.mode.get())
        self.trigger()

        

        # self.mode.put(self.params["K2100Params"]["children"][1]["value"])

        # self.mode.put(self.params["K2100Params"]["mode"]["value"])
        # self._driver.set_mode(self.mode)

    
    def measure(self):
        voltage = self._driver.read()   
        # self.voltage.put(voltage)
        print(f"Voltage: {voltage}")
        return voltage
        # self.voltage.put(self._driver.read())
        # return self.voltage.get()

    def commit_settings(self):
        mode_str = next(item for item in self.params["K2100Params"]["children"] if item["name"] == "mode")
        if self.mode.get() != mode_str["value"]:
            self._driver.set_mode(mode_str["value"])
            self.mode.put(mode_str["value"])
        # elif self.voltage.get() != self.params["voltage"]["value"]:
        #     self.voltage.put(self.voltage.get())
            
    
    # def trigger(self):
    #     self._driver.read()
    
    def measure_voltage(self):
        self.voltage.put(self._driver.measure_voltage())

#     def _contonious_read(self):
#         while not self._stop_event.is_set():
#             self.read()
#             time.sleep(1)
    
#     def start_continuous_read(self):
#         if self._thread is None:
#             self._stop_event.clear()
#             self._thread = threading.Thread(target=self._contonious_read)
#             self._thread.start()
    
#     def stop_continuous_read(self):
#         if self._thread is not None:
#             self._stop_event.set()
#             self._thread.join()
#             self._thread = None

# if __name__ == "__main__":
#     # logging.basicConfig(level=logging.INFO)
#     keithley = Keithley2100(name="keithley2100")
#     keithley.start_continuous_read()
#     try:
#         while True:
#             time.sleep(1)
#     except KeyboardInterrupt:
#         keithley.stop_continuous_read()

if __name__ == "__main__":
    from interface_Keithely2100 import Keithley2100
    keithley = Keithley2100(name="keithley")

    from bluesky import RunEngine

    RE = RunEngine({})
    from bluesky.callbacks.best_effort import BestEffortCallback

    bec = BestEffortCallback()

    # Send all metadata/data captured to the BestEffortCallback.
    RE.subscribe(bec)

    from bluesky.utils import ProgressBarManager

    RE.waiting_hook = ProgressBarManager()

    from bluesky.plans import count

    # from ophyd.sim import det1, det2  # two simulated detectors
    # dets = [det1, det2]   # a list of any number of detectors
    # RE(count(dets))

    # dets = [keithley.voltage]  # a list of any number of detectors

    dets = [keithley]
    RE(count(dets))