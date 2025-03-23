# Ophyd based actuators for Zaber devices 

from ophyd import Device, Component as Cpt, PVPositioner
from pybridge.hardware_bridge.zaber_PortDriver import ZaberConnection
import pyvisa
from zaber_motion import Tools
from ophyd.status import DeviceStatus, wait as status_wait
from ophyd import Signal, SignalRO
from ophyd import EpicsSignal
from ophyd import EpicsSignalRO
import logging

logger = logging.getLogger(__name__)


class ZaberConnect():
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ZaberConnect, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.zaber = None  # Drop down com port box to select which one to connect in GUI (For now we choose COM5 port)
            ports = Tools.list_serial_ports()
            for port in ports:
                if port == "COM5":
                    try:
                        self.zaber = ZaberConnection(port, 1)
                    except:
                        logger.error(f"Could not connect to Zaber device via {port}")
            self.initialized = True

# Bring all the Component objects and params into ZaberConnect class
class ZaberLinear(PVPositioner):
    setpoint = Cpt(Signal)
    readback = Cpt(SignalRO)
    done = Cpt(Signal, value=False)
    actuate = Cpt(Signal)
    stop_signal = Cpt(Signal)

    axis_index = Cpt(Signal, value=1, kind="config") # DK - this is more like an axis index. I suggest to rename it to axis_index that differentiates from axis_control.
    unit = Cpt(Signal, value="um", kind="config")

    def __init__(
            self,
            prefix="",
            *,
            limits=None,
            name=None,
            read_attrs=None,
            configuration_attrs=None,
            parent=None,
            egu="um", # DK - I noticed that this can be um or deg. We should set this later when axis_type is identified.
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
        self.zaber = ZaberConnect().zaber
        self.zaber.open_stage()
        self.axis_list = []
        self.axis_list.append(self.zaber.get_axis(self.axis_index.value))

    def set_axis(self, axis): 
        self.axis_list.append(axis)
        self.axis_index.put(len(self.axis_list) - 1)
    
    def get_axis(self):
        return self.axis_index.get()

    def get_position(self):
        return self.zaber.get_position(self.axis.value)

    def move(self, position):
        self.zaber.move_abs(position)
    def move_relative(self, position): 
        self.zaber.move_relative(position)
    def stop(self):
        self.zaber.stop()
    def home(self):
        self.zaber.home()

# DK - This is a duplicate class. I suggest to remove this class.
class ZaberRotary(PVPositioner):
    setpoint = Cpt(Signal)
    readback = Cpt(SignalRO)
    done = Cpt(Signal, value=False)
    actuate = Cpt(Signal)
    stop_signal = Cpt(Signal)
    axis_type = Cpt(SignalRO, value=2, kind="config")  # linear or rotary
    axis = Cpt(Signal, value=1, kind="config")  # axis number
    unit = Cpt(Signal, value="rad", kind="config")

    def __init__(
            self,
            prefix="",
            *,
            limits=None,
            name=None,
            read_attrs=None,
            configuration_attrs=None,
            parent=None,
            egu="deg",
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
        self.zaber = ZaberConnect().zaber
        self.open_stage()
        self.axis_list = [] 
        self.axis_list.append(self.zaber.get_axis(self.axis.value))
    
    def set_axis(self, axis): 
        self.axis_list.append(axis)
        self.axis_index.put(len(self.axis_list) - 1)
    
    def get_axis(self):
        return self.axis_index.get()

    def get_position(self):
        return self.zaber.get_position()
        
    def move(self, position):
        self.zaber.move_abs(position)
        
    def stop(self):
        self.zaber.stop()
    
    def move_relative(self, position):
        self.zaber.move_relative(position)
    
    def home(self): 
        self.zaber.home()
