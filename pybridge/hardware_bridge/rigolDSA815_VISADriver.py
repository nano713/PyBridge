from io import StringIO
import numpy as np
import pandas as pd
import pyvisa as visa

class RigolDSA815VISADriver:
    def __init__(self, driver):
        self.driver = driver
        self.dsa = None

    # "USB0::0x1AB1::0x0960::DSA8A154202508::INSTR"
      
    def connect(self):
        rm = visa.ResourceManager()
        self.dsa = rm.open_resource(self.driver)
        self.dsa.read_termination = '\n'
        self.dsa.write_termination = '\n'
        self.dsa.timeout = 10000  
    
    def set_start_frequency(self, frequency):
        self.dsa.write(f":SENS:FREQ:STAR {frequency}")
    
    def set_stop_frequency(self, frequency):
        self.dsa.write(f":SENS:FREQ:STOP {frequency}")
    
    def set_frequency_step(self, step): 
        self.dsa.write(f":SENS:FREQ:CENT:STEP:INCR {step}")
    
    def set_center_frequency(self, frequency):
        self.dsa.write(f":SENS:FREQ:CENT {frequency}")
    
    def set_sweep_time(self, time):
        self.dsa.write(f":SENS:SWE:TIME {time}")
    
    def set_frequency_points(self, points):
        if points < 101 or points > 3001:
            raise ValueError("Frequency points must be between 101 and 3001.")
        self.dsa.write(f":SENSe:SWEEp:POINts {points}")
    
    def get_start_frequency(self): # timeout error
        return int(self.dsa.query(":SENS:FREQ:STAR?"))
    
    def get_stop_frequency(self):
        return int(self.dsa.query(":SENS:FREQ:STOP?"))
    
    def get_frequency_step(self):
        return int(self.dsa.query(":SENS:FREQ:CENT:STEP:INCR?"))

    def get_center_frequency(self):
        return int(self.dsa.query(":SENS:FREQ:CENT?"))
    
    def get_sweep_time(self):
        return int(self.dsa.query(":SENS:SWE:TIME?"))
    
    def get_frequency_points(self): # timeout
        return int(self.dsa.query(":SENSe:SWEEp:POINts?"))
    
    
    def get_trace(self, number = 1):
        """ Returns a numpy array of the data for a particular trace
        based on the trace number (1, 2, or 3).
        """
        self.dsa.write(":FORMat:TRACe:DATA ASCII")
        raw_data = self.dsa.query(f":TRACE:DATA? TRACE{number}")
 
        try:
            numeric_data = raw_data.split(' ', 1)[-1]  
            data = np.array([float(x) for x in numeric_data.split(',') if x.strip()], dtype=np.float64)
        except ValueError as e:
            print(f"Error parising data: {e}")
            data = np.array([], dtype=np.int64)
        return data
     