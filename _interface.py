import logging
import time
from ophyd import Device, Component as Cpt, Signal, SignalRO
from ophyd.status import DeviceStatus
from keithley2100_VISADriver import Keithley2100VISADriver as Keithley

logger = logging.getLogger(__name__)

class Keithley2100(Device):
    voltage = Cpt(Signal, kind="hinted", metadata={"units": "V"})
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._driver = Keithley(self.params["resources"]["value"])
        self._driver.init_hardware()
        self.voltage.get = self.measure

        mode_string = next((item for item in self.params["K2100Params"]["children"] if item["name"] == "mode"))
        self.mode.put(mode_string["value"])
        self._driver.set_mode(self.mode.get())

    def measure(self):
        voltage = self._driver.read()
        return voltage

    def trigger(self):
        status = DeviceStatus(self)
        voltage = self.measure()
        self.voltage.put(voltage)
        self.voltage._run_subs(sub_type='value', old_value=None, value=voltage, timestamp=time.time())
        # print(f"Triggered Keithley2100: {voltage}")
        status.set_finished()
        return status

    def read(self):
        voltage = self.voltage.get()
        # print(f"Read voltage: {voltage}")
        return {
            'keithley_voltage': {
                'value': voltage,
                'timestamp': time.time(),
            }
        }

if __name__ == "__main__":
    from bluesky import RunEngine
    from bluesky.callbacks.best_effort import BestEffortCallback
    from bluesky.utils import ProgressBarManager
    from bluesky.plans import count
    from bluesky.callbacks import LiveTable
    from databroker import Broker

    from _interface import Keithley2100

    keithley = Keithley2100(name="keithley")

    RE = RunEngine({})

    bec = BestEffortCallback()
    RE.subscribe(bec)
    # token = RE.subscribe(LiveTable([keithley]))

    RE.waiting_hook = ProgressBarManager()

    # Configure Databroker
    db = Broker.named('temp')  # Use 'temp' catalog or replace with your catalog name
    RE.subscribe(db.insert)

    # RE(count([keithley], num=5, delay=0.1))

    print(f"keithley.read(): {keithley.read()}")
    print(f"keithley.get(): {keithley.get()}")
    print(f"keithley.voltage: {keithley.voltage.get()}")

    from ophyd.sim import motor
    from bluesky.plans import scan

    RE(scan([keithley], motor, -1, 1, 10))