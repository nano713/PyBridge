from ophyd import Component as Cpt
from ophyd import Device, Signal
from ophyd import SignalRO


class DSA815ViewBridge(Device):
    wavelength = Cpt(SignalRO, kind="hinted", metadata={"units": "nm"})
    frequency = Cpt(SignalRO, kind="hinted", metadata={"units": "Hz"})
    amplitude = Cpt(SignalRO, kind="hinted", metadata={"units": "dBm"})
    mode = Cpt(Signal, value="VOLT:DC", kind="config")


    def __init__(
            self,
            prefix="",
            *,
            name,
            parent=None, kind=None,
            driver = None,
            **kwargs,
    ):
        super().__init__(name=name, parent=parent, kind=kind, **kwargs)
    
        self.dsa815 = driver
