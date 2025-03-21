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
            self.zaber = None #Drop down com port box to select which one to connect in GUI (For now we choose COM5 port)
            rm = pyvisa.ResourceManager()
            ports = Tools.list_serial_ports()
            for port in ports:
                if port == "COM5":
                    try:
                        self.zaber = ZaberMultiple()
                        self.zaber.connect(port)
                    
                    except:
                        logger.error(f"Could not connect to Zaber device via {port}")
            self.initialized = True
                

class ZaberLinear(PVPositioner):
        setpoint = Cpt(Signal)
        readback = Cpt(SignalRO)
        done = Cpt(Signal, value = False)
        actuate = Cpt(Signal)
        stop_signal = Cpt(Signal)

        axis = Cpt(Signal, value = 1, kind = "config")
        unit = Cpt(Signal, value = "um", kind = "config")
        # params = [{'title': 'COM Port:', 'name': 'com_port', 'type': 'list', 'limits': ports, 'value': port},
        #         {'title': 'Controller:', 'name': 'controller_str', 'type': 'str', 'value': ''},
        #         {'title': 'Stage Properties:', 'name': 'stage_properties', 'type': 'group', 'children': [
        #             {'title': 'Stage Name:', 'name': 'stage_name', 'type': 'str', 'value': '', 'readonly': True},
        #             {'title': 'Stage Type:', 'name': 'stage_type', 'type': 'str', 'value': '', 'readonly': True}]}
        #         ]  

        def __init__(
            self,
            prefix="",
            *,
            limits=None,
            name=None,
            read_attrs=None,
            configuration_attrs=None,
            parent=None,
            egu="um",
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
        def get_position(self):
            return self.zaber.get_position(self.axis.value)

class ZaberRotary(PVPositioner): 
    setpoint = Cpt(Signal)
    readback = Cpt(SignalRO)
    done = Cpt(Signal, value = False)
    actuate = Cpt(Signal)
    stop_signal = Cpt(Signal)
    axis_type = Cpt(SignalRO, value = 2, kind = "config") # linear or rotary
    axis = Cpt(Signal, value = 1, kind = "config") # axis number
    unit = Cpt(Signal, value = "rad", kind = "config")

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
    