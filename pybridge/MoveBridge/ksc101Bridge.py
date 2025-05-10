from ophyd.signal import Signal, SignalRO
from ophyd import Device, Component as Cpt
from ophyd.pv_positioner import PVPositioner
from pybridge.hardware_bridge.ksc101_VISADriver import KSC101

class KSC101ViewBridge(Device):
    """
    Class to control the KSC101 via the Solenoid Driver.
    """
    state = Cpt(SignalRO, value = False, kind='normal')
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
        self.ksc101 = KSC101(serial = driver) 
        self.state.get = self.get_shutter_state
    
    def open_shutter(self):
        """
        Open the shutter.
        """
        self.ksc101.open_shutter()
    
    def close_shutter(self):
        """
        Close the shutter.
        """
        self.ksc101.close_shutter()
    
    def get_shutter_state(self):
        """
        Get the state of the shutter.
        """
        state = self.ksc101.get_shutter_state()
        if state == "Active":
            return True
        elif state == "Inactive":
            return False
        else:
            raise ValueError(f"Unknown state: {state}")
    
    def close(self):
        """
        Close the connection to the KSC101.
        """
        self.ksc101.disconnect()
    