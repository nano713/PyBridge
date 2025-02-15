from keithley2100_VISADriver import Keithley2100VISADriver as Keithley
from ophyd import Device, Component as Cpt, Signal, SignalRO


class Keithley2100(Device):

    voltage = Cpt(SignalRO, value=0.0, name="voltage")
    mode = Cpt(Signal, value="VOLT:DC", name="mode")

    params = { [
        {
            "title": "Resources",
            "name": "resources",
            "type": "str",
            "value": "USB0::0x05E6::0x2100::1149087::INSTR",
        },
        {
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
                    "value": "VDC",
                },
            ] } ] }
    
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
        self._driver = Keithley()
        self._driver.open_resource(self.resources)
        self.mode.put(self.params["K2100Params"]["mode"]["value"])
        self._driver.set_mode(self.mode)
    
    def read(self):
        return self._driver.read()
    
    def commit_settings(self):
        if self.mode.get() != self.params["K2100Params"]["mode"]["value"]:
            self._driver.set_mode(self.params["K2100Params"]["mode"]["value"])
