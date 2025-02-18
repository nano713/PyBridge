import logging

from ophyd import Device, Component as Cpt, Signal, SignalRO
from pymeasure.instruments.keithley.keithley2000 import Keithley2000 #Keithley2000 works for Keithley2100
# import pyvisa

logger = logging.getLogger(__name__)

class Keithley2100(Device):

    voltage = Cpt(Signal, name="voltage")
    mode = Cpt(Signal, value="VOLT:DC", name="mode")

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
                    "limits": ["VDC", "VAC", "R2W", "R4W", "IDC", "IAC"],
                    # ValueError: Value of voltage` is not in the discrete set {'current': 'CURR:DC', 'current ac': 'CURR:AC', 'voltage': 'VOLT:DC', 'voltage ac': 'VOLT:AC', 'resistance': 'RES', 'resistance 4W': 'FRES', 'period': 'PER', 'frequency': 'FREQ', 'temperature': 'TEMP', 'diode': 'DIOD', 'continuity': 'CONT'}
                    "value": "VDC",
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
        self._driver = Keithley2000(self.params["resources"]["value"])
        # self.voltage.get(self._driver.voltage)
        self.voltage.get = lambda: self._driver.voltage

        # self.mode.put(self.params["K2100Params"]["children"][1]["value"])

        # self.mode.put(self.params["K2100Params"]["mode"]["value"])
        # self._driver.set_mode(self.mode)

        # self.voltage.put(self._driver.read())
        
    # def init_hardware(self):
    #     """Initialize the selected VISA resource
        
    #     :param pyvisa_backend: Expects a pyvisa backend identifier or a path to the visa backend dll (ref. to pyvisa)
    #     :type pyvisa_backend: string
    #     """
    #     self.rm = pyvisa.highlevel.ResourceManager()
    #     self._instr = self.rm.open_resource(self.params["resources"]["value"],``
    #                                        write_termination="\n",
    #                                        )    
    
    def read(self):
        return self._driver.read()

    def commit_settings(self):
        if self.mode.get() != self.params["K2100Params"]["mode"]["value"]:
            self._driver.set_mode(self.params["K2100Params"]["mode"]["value"])
            self.mode.put(self.params["K2100Params"]["mode"]["value"])
    
    def trigger(self):
        self._driver.trigger()
    
    def measure_voltage(self):
        self.voltage.put(self._driver.measure_voltage())
