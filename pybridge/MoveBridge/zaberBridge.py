# Ophyd based actuators for Zaber devices 

from ophyd import Device, Component as Cpt, PVPositioner
from ophyd.status import DeviceStatus, wait as status_wait
from ophyd import Signal, SignalRO
from ophyd import EpicsSignal
from ophyd import EpicsSignalRO

class ZaberConnect(): 
    def __init__(self): 
        self.zaber = None #Drop down com port box to select which one to connect in GUI (For now we choose COM5 port)
        possible_ports = rm.list_resources()
        ports = [port.device for port in possible_ports]
        for port in ports:
            try:
                self.zaber = ZaberMultiple()
                self.zaber.connect(port)
                logger.info(f"Connected to Zaber device on port {port}")
                break
            except ZaberError as e:
                
class ZaberLinear(PVPositioner):

    setpoint = Cpt(Signal)
    readback = Cpt(SignalRO)
    done = Cpt(Signal, value = False)
    actuate = Cpt(Signal)
    stop_signal = Cpt(Signal)

    axis_type = Cpt(Signal, value = 1, kind = "config")
    unit = Cpt(Signal, value = "um", kind = "config")
    params = [{'title': 'COM Port:', 'name': 'com_port', 'type': 'list', 'limits': ports, 'value': port},
              {'title': 'Controller:', 'name': 'controller_str', 'type': 'str', 'value': ''},
              {'title': 'Stage Properties:', 'name': 'stage_properties', 'type': 'group', 'children': [
                  {'title': 'Stage Name:', 'name': 'stage_name', 'type': 'str', 'value': '', 'readonly': True},
                  {'title': 'Stage Type:', 'name': 'stage_type', 'type': 'str', 'value': '', 'readonly': True}]}
              ]  

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
        self.zaber = None
        possible_ports = rm.list_resources()
        ports = [port.device for port in possible_ports]
        for port in ports:
            try:
                self.zaber = ZaberMultiple()
                self.zaber.connect(port)
                
                zaber.connect()
                zaber.disconnect()
            except:
                ports.remove(port)

class ZaberRotary(PVPositioner): 
    setpoint = Cpt(Signal)
    readback = Cpt(SignalRO)
    done = Cpt(Signal, value = False)
    actuate = Cpt(Signal)
    stop_signal = Cpt(Signal)

    axis_type = Cpt(SignalRO)
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