import numpy as np
from ophyd import Device, Component as Cpt, Signal, SignalRO
from ophyd.status import MoveStatus
from pymeasure.instruments.srs import SR830

class SR830Viewer(Device):
    filter_slope = Cpt(Signal, value = 0, kind = "config")
    frequency = Cpt(Signal, value = 0, kind = "config")
    lia_status = Cpt(Signal, value = "True", kind = "config")
    filter_slope = Cpt(Signal, value = 0, kind = "config")
    reference_source = Cpt(Signal, value = 0, kind = "config")
    reference_source_trigger = Cpt(Signal, value = 0, kind = "config")
    sensitivity = Cpt(Signal, value = 0, kind = "config")
    time_constant = Cpt(Signal, value = 0, kind = "config")

    err_status = Cpt(SignalRO, value = 0, kind = "hinted")
    is_out_of_range = Cpt(SignalRO, value = 0, kind = "hinted")
    id = Cpt(SignalRO, value = 0, kind = "hinted")
    x = Cpt(SignalRO, value = 0, kind = "hinted")
    y = Cpt(SignalRO, value = 0, kind = "hinted")
    r = Cpt(SignalRO, value = 0, kind = "hinted")
    theta = Cpt(SignalRO, value = 0, kind = "hinted")
    
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
        super().__init__(
            prefix=prefix,
            name=name,
            read_attrs=read_attrs,
            configuration_attrs=configuration_attrs,
            parent=parent,
            **kwargs,
        )

        # self.image.get = self.get_image
        # self.image.put = self.set_image
        # self.spectrum.get = self.get_spectrum

    def set_harmonics(self):
        pass
    
    def get_harmonics(self):
        pass
    
    def reset(self):
        pass 
    
    def snap(self): 
        pass 

    def get_image(sel):
        pass 
    def snap(self):
        pass
        
