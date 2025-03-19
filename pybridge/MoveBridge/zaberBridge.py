# Ophyd based actuators for Zaber devices 

from ophyd import Device, Component as Cpt, PVPositioner
from ophyd.status import DeviceStatus, wait as status_wait
from ophyd import Signal
from ophyd import EpicsSignal
from ophyd import EpicsSignalRO

class ZaberStage(PVPositioner)