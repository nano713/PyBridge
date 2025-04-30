from ophyd import Component as Cpt
from ophyd import Device, Signal
from ophyd import SignalRO
from pybridge.hardware_bridge.rigolDSA815_VISADriver import RigolDSA815 as DSA815


class DSA815ViewBridge(Device):
    wavelength = Cpt(SignalRO, kind="hinted", metadata={"units": "nm"})
    frequency = Cpt(SignalRO, kind="hinted", metadata={"units": "Hz"})
    amplitude = Cpt(SignalRO, kind="hinted", metadata={"units": "dBm"})


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
    
        self.dsa815 = DSA815()
        
