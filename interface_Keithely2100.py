from keithley2100_VISADriver import Keithley2100VISADriver as Keithley
from ophyd import Device, Component as Cpt, Signal, SignalRO


class Keithley2100(Device):

    voltage = Cpt(SignalRO, value=0.0, name="voltage")
    mode = Cpt(Signal, value="VOLT:DC", name="mode")
    
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
): super().__init__(name=name, parent=parent, kind=kind, **kwargs)
    
