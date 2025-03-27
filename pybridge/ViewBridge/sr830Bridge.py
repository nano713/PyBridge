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
        self.x.get, self.y.get, self.theta.get = self.get_measurements
        self.lia_status.get = self.get_lia_status
        self.time_constant.put = self.set_time_constant
        self.sensitivity.pyt = self.set_senstivity
        self.r.get = self.calculate_r
        self.filter_slope.put = self.set_filter_slope
        self.frequency.put = self.set_frequency
        
        

        # self.image.get = self.get_image
        # self.image.put = self.set_image
        # self.spectrum.get = self.get_spectrum

    def set_harmonics(self):
        self.sr830.harmonic = self.harmonic.get()
    
    def set_filter_slope(self):
        self.sr830.filter_slope = self.filter_slope.get()

    def set_frequency(self):
        self.sr830.frequency = self.frequency.get()
    
    def get_lia_status(self):
        return self.sr830.lia_status
    
    def get_theta(self):
        return self.sr830.theta
    
    def get_harmonics(self):
        return self.sr830.harmonic

    def get_identification(self):
        return self.sr830.id
       
    def reset(self):
        self.sr830.reset()
    
    def get_is_out_of_range(self):
        range = self.sr830.is_out_of_range
        if range == "True":
            logger.warning*("SR830 is out of range")
        else:
            logger.info("SR830 is in range")
        return range
    def calculate_r(self): 
        x = self.x.get()
        y = self.y.get()
        r = np.sqrt(x**2 + y**2)
        return r
    
    def get_measurements(self): 
        x = self.sr830.x()
        y = self.sr830.y()
        theta = self.sr830.theta
        return x, y, theta
    def set_time_constant(self):
        self.sr830.time_constant(self.time_constant.get())
    
    def set_senstivity(self): 
        self.sr830.sensitivity(self.sensitivity.get())

    def get_image(self):
        self.sr830.start_scan() 
        data = self.sr830.snap(self.x.get(), self.y.get())
        return data
