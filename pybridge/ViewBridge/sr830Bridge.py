import numpy as np
from ophyd import Device, Component as Cpt, Signal, SignalRO
from ophyd.status import MoveStatus
from pymeasure.instruments.srs import SR830
import logging 
logger = logging.getLogger(__name__) 

class SR830Viewer(Device):
    filter_slope = Cpt(Signal, value = 0, kind = "config")
    frequency = Cpt(Signal, value = 0, kind = "config")
    lia_status = Cpt(SignalRO, value = "True", kind = "config") 
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
        #Getter Components


        #Setter Components
        self.sr830 = SR830(self.port.get())
        self.harmonic.put = self.set_harmonics
        self.harmonic.get = self.get_harmonics
        self.x.get = self.get_x_value
        self.y.get = self.get_y_value
        self.theta.get = self.get_theta
        self.lia_status.get = self.get_lia_status
        self.time_constant.put = self.set_time_constant
        self.time_constant.get = self.get_time_constant
        self.sensitivity.put = self.set_senstivity
        self.sensitivity.get = self.get_sensitivity
        self.r.get = self.calculate_r
        self.filter_slope.put = self.set_filter_slope
        self.filter_slope.get = self.get_filter_slope
        self.frequency.put = self.set_frequency
        self.frequency.get = self.get_frequency
        self.reference_source.put = self.set_resource_source
        self.reference_source_trigger.put = self.set_resource_source_trigger
        self.err_status.get = self.get_err_status

        self.id.get = self.get_identification
        

    def set_harmonics(self, harmonic):
        """Set the harmonic of the SR830 lock-in amplifier."""
        if isinstance(harmonic, float): 
            harmonic = int(harmonic)
            self.sr830.harmonic = harmonic
            logger.info(f"Harmonic set to {harmonic}.")
        elif isinstance(harmonic, int) and harmonic > 0:
            self.sr830.harmonic = harmonic
            logger.info(f"Harmonic set to {harmonic}.")
        else:
            logger.error("Harmonic must be an integer.")
    
    def get_harmonics(self):
        """Get the current harmonic of the SR830 lock-in amplifier."""
        return self.sr830.harmonic

    def set_resource_source_trigger(self, source):
        """Set the reference source trigger of the SR830 lock-in amplifier.
        Args:
            source (str): The reference source trigger to set. Can be "SINE", "POS EDGE", or "NEG EDGE".
        """
        if source == "SINE" or source == "POS EDGE" or source == "NEG EDGE":
            self.sr830.reference_source_trigger = source
        else:
            logger.error("Invalid source. Please choose from 'SINE', 'POS EDGE', or 'NEG EDGE'.")
    
    def get_resource_source_trigger(self):
        """Get the current reference source trigger of the SR830 lock-in amplifier.
        Returns:
            str: The current reference source trigger.
        """
        return self.sr830.reference_source_trigger

    def set_resource_source(self, source):
        """Set the reference source of the SR830 lock-in amplifier.
        Args:
            source (str): The reference source to set. Can be "Internal" or "External".
        """
        if source == "Internal" or source == "External":
            self.sr830.reference_source = source
        else:
            logger.error("Invalid source. Please choose from 'Internal' or 'External'.")

    def get_resource_source(self):
        """Get the current reference source of the SR830 lock-in amplifier.
        Returns:
            str: The current reference source.
        """
        return self.sr830.reference_source        
    
    def set_filter_slope(self, slope):
        """Set the filter slope of the SR830 lock-in amplifier.
        Args:
            slope (int): The filter slope to set. Can be 6, 12, 18, or 24 dB/octave.
        """
        self.sr830.filter_slope = slope
    
    def get_filter_slope(self):
        """Get the current filter slope of the SR830 lock-in amplifier.
        Returns:
            int: The current filter slope.
        """
        return self.sr830.filter_slope

    def set_frequency(self, frequency):
        """Set the frequency of the SR830 lock-in amplifier."""
        self.sr830.frequency = frequency
        logger.info(f"Frequency set to {frequency}.")
    def get_frequency(self):
        """Get the current frequency of the SR830 lock-in amplifier.
        Returns:
            float: The current frequency.
        """
        return self.sr830.frequency
    
    def get_lia_status(self):
        """Get the current lock-in amplifier status of the SR830.
        Returns:
            str: The current lock-in amplifier status.
        """
        return self.sr830.lia_status
    
    def get_theta(self):
        """Get the current theta value of the SR830 lock-in amplifier
        returns:
            float: The current theta value.
        """
        return self.sr830.theta
    

    def get_identification(self):
        """Get the identification of the SR830 lock-in amplifier.
        Returns:
            str: The identification of the SR830.
        """
        return self.sr830.id
       
    def reset(self):
        """Reset the SR830 lock-in amplifier."""
        self.sr830.reset()
    def get_err_status(self):
        """Get the error status of the SR830 lock-in amplifier."
        returns:
            str: The error status of the SR830.
        """
        return self.sr830.err_status 
    
    def get_is_out_of_range(self):
        """Get the out of range status of the SR830 lock-in amplifier.
        returns:
            str: The out of range status of the SR830.
        """
        range = self.sr830.is_out_of_range
        if range == "True":
            logger.warning*("SR830 is out of range")
        else:
            logger.info("SR830 is in range")
        return range
    
    def calculate_r(self): 
        """Calculate the magnitude of the signal from the x and y components.
        Returns:
            float: The magnitude of the signal.
        """
        x = self.x.get()
        y = self.y.get()
        r = np.sqrt(x**2 + y**2)
        return r
    
    def get_x_value(self):
        """Get X values from the SR830
        Returns:
            x (int): x value in volts
        """
        return self.sr830.x
    def get_y_value(self): 
        """Get Y values from SR830
        Returns:
            y (int): y value in volts
        """
        return self.sr830.y
                                                    
    def set_time_constant(self, time_constant):
        """Set the time constant of the SR830 lock-in amplifier."""
        self.sr830.time_constant = time_constant
    def get_time_constant(self):
        """Get the current time constant of the SR830 lock-in amplifier.
        Returns:
            float: The current time constant.
        """
        return self.sr830.time_constant
    def get_sensitivity(self):
        """Get the current sensitivity of the SR830 lock-in amplifier.
        Returns:
            float: The current sensitivity.
        """
        return self.sr830.sensitivity
    
    def set_senstivity(self, sensitivity): 
        """Set the sensitivity of the SR830 lock-in amplifier."""
        self.sr830.sensitivity = sensitivity

    def set_quick_range(self):
        """Adjust the Sensitivity of SR830
        Args:
            range: value to set the range"""
        self.sr830.quick_range()
    def get_image(self, parameter1, parameter2):
        """Get the image from the SR830 lock-in amplifier.
        Returns:
            numpy.ndarray: The image data.

        Method that records and retrieves 2 to 6 parameters at a single
        instant. The parameters can be one of: X, Y, R, Theta, Aux In 1,
        Aux In 2, Aux In 3, Aux In 4, Frequency, CH1, CH2.
        Default is "X" and "Y".            
        """
        if parameter1 and parameter2 in ["X", "Y", "R", "Theta", "Aux In 1", "Aux In 2", "Aux In 3", "Aux In 4", "Frequency", "CH1", "C"]:
            self.sr830.start_scan() 
            data = self.sr830.snap(parameter1, parameter2)
            return data
