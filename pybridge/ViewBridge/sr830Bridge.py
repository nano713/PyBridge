import numpy as np
from ophyd import Device, Component as Cpt, Signal, SignalRO
from ophyd.status import MoveStatus
from pymeasure.instruments.srs import SR830
import logging 
logger = logging.getLogger(__name__) 

class SR830Viewer(Device):
    filter_slope = Cpt(Signal, value = 0, kind = "config")
    frequency = Cpt(Signal, value = 0, kind = "config")
    lia_status = Cpt(Signal, value = "True", kind = "config")
    reference_source = Cpt(Signal, value = 0, kind = "config")
    reference_source_trigger = Cpt(Signal, value = 0, kind = "config")
    sensitivity = Cpt(Signal, value = 0, kind = "config")
    time_constant = Cpt(Signal, value = 0, kind = "config")
    harmonic = Cpt(Signal, value = 0, kind = "config")

    err_status = Cpt(SignalRO, value = 0, kind = "config")
    is_out_of_range = Cpt(SignalRO, value = 0, kind = "config")
    id = Cpt(SignalRO, value = 0, kind = "config")
    x = Cpt(SignalRO, value = 0, kind = "hinted")
    y = Cpt(SignalRO, value = 0, kind = "hinted")
    r = Cpt(SignalRO, value = 0, kind = "hinted")
    theta = Cpt(SignalRO, value = 0, kind = "hinted")
    port = Cpt(Signal, value = "GPIB0::1::INSTR", kind = "config")
    
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
        # port = "",
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
        self.sr830 = SR830(self.port.get())
        self.harmonic.put = self.set_harmonics
        self.harmonic.get = self.get_harmonics
        self.theta.get = self.get_theta
        
        

        # self.image.get = self.get_image
        # self.image.put = self.set_image
        # self.spectrum.get = self.get_spectrum

    def set_harmonics(self):
        self.sr830.harmonic(self.harmonic.get())
    
    def get_theta(self):
        return self.sr830.theta
    
    def get_harmonics(self):
        return self.sr830.harmonic

    def get_identification(self):
        return self.sr830.id
        # logger.info(f"SR830 Identification: " + {self.sr830.id()})    
    def reset(self):
        pass 

    def get_image(sel):
    #     pass 
    # def snap(self):
    #     self.sr830.snap(val1 = "X", val2 = "Y")
    #     # self.sr830.start_scan()
