#
# This file is part of the PyMeasure package.
#
# Copyright (c) 2013-2024 PyMeasure Developers
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

from pymeasure.instruments import Instrument
from pymeasure.instruments.validators import truncated_range

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
    
    # def get_trace(self, number = 1):
    #     """ Returns a numpy array of the data for a particular trace
    #     based on the trace number (1, 2, or 3).
    #     """
    #     self.dsa.write(":FORMat:TRACe:DATA ASCII")
    #     raw_data = self.dsa.query(f":TRACE:DATA? TRACE{number}")

        try:
            data = np.array([int(float(x)) for x in raw_data.split(',') if x.strip()], dtype=np.int64)
        except ValueError as e:
            print(f"Error parising data: {e}")
            data = np.array([], dtype=np.int64)
        return data
    
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
     
    
"""'#9000009014 -3.242744e+00, -5.416249e+01, -5.649438e+01, -5.631198e+01, -5.578156e+01, -5.571463e+01, -5.498612e+01, -5.541377e+01, -5.550010e+01, -5.670262e+01, -5.508814e+01, -5.499963e+01, -5.526011e+01, -5.566027e+01, -5.477467e+01, -5.523911e+01, -5.470570e+01, -5.437718e+01, -5.610948e+01, -5.467702e+01, -5.427193e+01, -5.532796e+01, -5.491653e+01, -5.564345e+01, -5.602866e+01, -5.464831e+01, -5.624313e+01, -5.459763e+01, -5.414645e+01, -5.520468e+01, -5.621841e+01, -5.590670e+01, -5.559005e+01, -5.361253e+01, -5.584196e+01, -5.542259e+01, -5.522298e+01, -5.522801e+01, -5.556039e+01, -5.570082e+01, -5.544695e+01, -5.593282e+01, -5.540948e+01, -5.516024e+01, -5.489001e+01, -5.494830e+01, -5.585099e+01, -5.511798e+01, -5.537524e+01, -5.285376e+01, -5.552083e+01, -5.563908e+01, -5.407242e+01, -5.485728e+01, -5.605648e+01, -5.570994e+01, -5.499692e+01, -5.504352e+01, -5.557335e+01, -5.612957e+01, -5.424394e+01, -5.636638e+01, -5.608711e+01, -5.488775e+01, -5.424888e+01, -5.575211e+01, -5.496731e+01, -5.501259e+01, -5.344410e+01, -5.489431e+01, -5.460674e+01, -5.480939e+01, -5.336911e+01, -5.544057e+01, -5.377362e+01, -5.473156e+01, -5.553797e+01, -5.593990e+01, -5.484823e+01, -5.482108e+01, -5.554324e+01, -5.477119e+01, -5.388068e+01, -5.559732e+01, -5.489148e+01, -5.586623e+01, -5.563022e+01, -5.530062e+01, -5.535039e+01, -5.500202e+01, -5.583103e+01, -5.468172e+01, -5.478651e+01, -5.371200e+01, -5.480054e+01, -5.567157e+01, -5.385327e+01, -5.617110e+01, -5.529262e+01, -5.576373e+01, -5.513307e+01, -5.468568e+01, -5.335184e+01, -5.512778e+01, -5.440955e+01, -5.559236e+01, -5.598184e+01, -5.608970e+01, -5.419023e+01, -5.578565e+01, -5.616304e+01, -5.419844e+01, -5.429643e+01, -5.436660e+01, -5.522842e+01, -5.463262e+01, -5.399570e+01, -5.635400e+01, -5.516724e+01, -5.645748e+01, -5.418272e+01, -5.483788e+01, -5.503821e+01, -5.414497e+01, -5.456636e+01, -5.478902e+01, -5.474881e+01, -5.568424e+01, -5.446713e+01, -5.433537e+01, -5.434738e+01, -5.461505e+01, -5.414804e+01, -5.479181e+01, -5.530385e+01, -5.505826e+01, -5.547099e+01, -5.519358e+01, -5.473314e+01, -5.542505e+01, -5.562563e+01, -5.438443e+01, -5.462541e+01, -5.523761e+01, -5.427679e+01, -5.563054e+01, -5.436128e+01, -5.513645e+01, -5.557238e+01, -5.535352e+01, -5.518504e+01, -5.410949e+01, -5.603259e+01, -5.489454e+01, -5.472084e+01, -5.516320e+01, -5.550692e+01, -5.346099e+01, -5.455022e+01, -5.450203e+01, -5.636536e+01, -5.509628e+01, -5.484324e+01, -5.469774e+01, -5.450862e+01, -5.491814e+01, -5.415907e+01, -5.623418e+01, -5.507316e+01, -5.488928e+01, -5.490413e+01, -5.399506e+01, -5.599226e+01, -5.458056e+01, -5.353281e+01, -5.547926e+01, -5.564382e+01, -5.496417e+01, -5.461482e+01, -5.660995e+01, -5.475008e+01, -5.565265e+01, -5.486929e+01, -5.493086e+01, -5.312734e+01, -5.415266e+01, -5.635369e+01, -5.509168e+01, -5.466945e+01, -5.555981e+01, -5.544144e+01, -5.511732e+01, -5.432343e+01, -5.512654e+01, -5.377093e+01, -5.649896e+01, -5.557578e+01, -5.475931e+01, -5.533873e+01, -5.488917e+01, -5.623963e+01, -5.410363e+01, -5.488480e+01, -5.416996e+01, -5.442680e+01, -5.609862e+01, -5.485405e+01, -5.471628e+01, -5.489852e+01, -5.508057e+01, -5.311176e+01, -5.367570e+01, -5.385984e+01, -5.560744e+01, -5.560450e+01, -5.590645e+01, -5.429300e+01, -5.559098e+01, -5.548669e+01, -5.555956e+01, -5.535353e+01, -5.602278e+01, -5.564784e+01, -5.466105e+01, -5.437751e+01, -5.460036e+01, -5.423131e+01, -5.375058e+01, -5.528915e+01, -5.463158e+01, -5.547705e+01, -5.280145e+01, -5.587578e+01, -5.457156e+01, -5.562926e+01, -5.420277e+01, -5.573685e+01, -5.335420e+01, -5.524068e+01, -5.312155e+01, -5.420966e+01, -5.407639e+01, -5.428963e+01, -5.323083e+01, -5.503064e+01, -5.436312e+01, -5.583693e+01, -5.476875e+01, -5.569872e+01, -5.467146e+01, -5.546909e+01, -5.538469e+01, -5.553432e+01, -5.632607e+01, -5.592004e+01, -5.581165e+01, -5.454325e+01, -5.363921e+01, -5.532804e+01, -5.407662e+01, -5.342876e+01, -5.612113e+01, -5.608727e+01, -5.412911e+01, -5.575197e+01, -5.567506e+01, -5.532588e+01, -5.477260e+01, -5.648471e+01, -5.551202e+01, -5.654199e+01, -5.636215e+01, -5.278934e+01, -5.686957e+01, -5.613879e+01, -5.580572e+01, -5.580516e+01, -5.388899e+01, -5.454232e+01, -5.677266e+01, -5.532428e+01, -5.529934e+01, -5.652688e+01, -5.380827e+01, -5.519189e+01, -5.553362e+01, -5.580663e+01, -5.468913e+01, -5.523951e+01, -5.497224e+01, -5.511716e+01, -5.539957e+01, -5.576390e+01, -5.330897e+01, -5.329752e+01, -5.502947e+01, -5.477116e+01, -5.581381e+01, -5.442037e+01, -5.468797e+01, -5.386069e+01, -5.460800e+01, -5.516819e+01, -5.561367e+01, -5.551629e+01, -5.589432e+01, -5.471980e+01, -5.190845e+01, -5.484184e+01, -5.422612e+01, -5.580157e+01, -5.515262e+01, -5.402090e+01, -5.497296e+01, -5.455679e+01, -5.530065e+01, -5.596619e+01, -5.437643e+01, -5.414277e+01, -5.491098e+01, -5.429411e+01, -5.310906e+01, -5.396264e+01, -5.400498e+01, -5.339393e+01, -5.114213e+01, -5.553609e+01, -5.325797e+01, -5.432230e+01, -5.571265e+01, -5.432244e+01, -5.405312e+01, -5.505526e+01, -5.374396e+01, -5.272102e+01, -5.354709e+01, -5.361119e+01, -5.379070e+01, -5.301088e+01, -5.521793e+01, -5.201998e+01, -5.391175e+01, -5.276485e+01, -5.500291e+01, -5.296730e+01, -5.473509e+01, -5.430976e+01, -5.273492e+01, -5.454482e+01, -5.528027e+01, -5.528080e+01, -5.364985e+01, -5.446684e+01, -5.405797e+01, -5.233681e+01, -5.366286e+01, -5.356519e+01, -5.360024e+01, -5.270844e+01, -5.192131e+01, -5.500739e+01, -5.280469e+01, -5.329724e+01, -5.166524e+01, -5.123502e+01, -5.169364e+01, -5.224844e+01, -5.197272e+01, -5.197606e+01, -5.041739e+01, -5.117262e+01, -5.049770e+01, -5.335361e+01, -5.226528e+01, -5.303884e+01, -5.335412e+01, -5.324722e+01, -5.222999e+01, -5.148598e+01, -5.289656e+01, -5.270380e+01, -5.188836e+01, -5.144784e+01, -5.235815e+01, -5.319089e+01, -5.251703e+01, -5.302527e+01, -5.270902e+01, -5.262627e+01, -5.346257e+01, -5.330931e+01, -5.313609e+01, -5.215028e+01, -5.226333e+01, -5.248144e+01, -5.250042e+01, -5.285648e+01, -5.258431e+01, -5.313704e+01, -5.230003e+01, -5.238030e+01, -5.058387e+01, -5.296836e+01, -5.126083e+01, -5.305616e+01, -5.276095e+01, -5.309354e+01, -4.974479e+01, -5.232188e+01, -5.309862e+01, -5.331057e+01, -5.151020e+01, -5.008195e+01, -5.158627e+01, -5.278719e+01, -5.226226e+01, -5.202507e+01, -5.165751e+01, -5.292997e+01, -5.109946e+01, -5.241528e+01, -5.284626e+01, -5.339019e+01, -5.208322e+01, -5.260498e+01, -5.155872e+01, -5.208007e+01, -5.168273e+01, -5.204307e+01, -5.285537e+01, -5.319736e+01, -5.335433e+01, -5.165339e+01, -5.178020e+01, -5.075055e+01, -5.182259e+01, -5.292930e+01, -5.147103e+01, -5.119794e+01, -5.114111e+01, -5.249058e+01, -5.038116e+01, -5.257013e+01, -5.265355e+01, -5.009803e+01, -5.169817e+01, -5.209117e+01, -4.913024e+01, -5.241844e+01, -5.116375e+01, -5.098901e+01, -5.047997e+01, -5.157015e+01, -5.009004e+01, -5.125986e+01, -5.219684e+01, -5.212345e+01, -4.928827e+01, -5.039126e+01, -5.202745e+01, -5.057165e+01, -4.950626e+01, -5.100826e+01, -5.269644e+01, -5.153149e+01, -5.034665e+01, -4.905051e+01, -5.138998e+01, -5.184852e+01, -4.955902e+01, -5.194352e+01, -5.239191e+01, -4.895700e+01, -5.146560e+01, -4.918729e+01, -5.010586e+01, -5.126611e+01, -5.076663e+01, -5.172609e+01, -5.034631e+01, -5.124309e+01, -5.107784e+01, -5.098313e+01, -4.984266e+01, -4.961209e+01, -4.989380e+01, -5.093864e+01, -5.063943e+01, -4.913616e+01, -5.089240e+01, -4.955770e+01, -4.919414e+01, -4.953192e+01, -4.799455e+01, -4.884472e+01, -4.789254e+01, -4.970940e+01, -4.851638e+01, -4.890857e+01, -5.017745e+01, -5.012514e+01, -4.988079e+01, -4.949535e+01, -4.973759e+01, -4.958575e+01, -4.888072e+01, -4.910970e+01, -5.025422e+01, -4.968306e+01, -5.010107e+01, -5.048270e+01, -4.911882e+01, -4.939202e+01, -5.011037e+01, -4.829499e+01, -5.012324e+01, -4.971426e+01, -5.013484e+01, -5.000364e+01, -5.042583e+01, -5.076597e+01, -4.870989e+01, -4.839778e+01, -4.981194e+01, -4.961653e+01, -4.770585e+01, -4.893539e+01, -4.997200e+01, -4.853645e+01, -4.960739e+01, -4.892692e+01, -5.026648e+01, -5.012748e+01, -4.951329e+01, -4.972636e+01, -4.780416e+01, -4.907436e+01, -4.847201e+01, -5.007944e+01, -5.001285e+01, -4.966423e+01, -5.015985e+01, -4.828648e+01, -4.899632e+01, -5.040811e+01, -4.987249e+01, -5.009517e+01, -5.025527e+01, -4.755337e+01, -4.919611e+01, -5.087989e+01, -4.790204e+01, -5.002255e+01, -4.906213e+01, -4.877286e+01, -5.020505e+01, -4.859045e+01, -5.080264e+01, -4.947663e+01, -4.897213e+01, -4.897013e+01, -4.996133e+01, -4.984718e+01, -4.858630e+01, -4.946822e+01, -4.943715e+01, -5.071580e+01, -5.008918e+01, -4.750502e+01, -4.833328e+01, -5.013039e+01, -5.021646e+01, -5.065741e+01, -4.848999e+01, -4.777668e+01, -4.765399e+01, -4.969319e+01, -4.872341e+01, -4.945744e+01, -4.861868e+01, -4.916101e+01, -4.953712e+01, -4.817685e+01, -4.819244e+01, -4.755506e+01, -4.656675e+01, -4.928949e+01, -4.727600e+01, -4.871386e+01, -4.920157e+01, -4.899684e+01, -4.908370e+01, -4.964863e+01, -4.878108e+01, -4.661673e+01, -4.767131e+01, -4.779600e+01, -4.667422e+01, -4.848033e+01, -4.822638e+01, -4.816923e+01'"""
    

class RigolDSA815(Instrument):
    """ Represents the RigolDSA815 Spectrum Analyzer
    and provides a high-level interface for taking scans of
    high-frequency spectra
    """

    start_frequency = Instrument.control(
        ":SENS:FREQ:STAR?", ":SENS:FREQ:STAR %e",
        """ A floating point property that represents the start frequency
        in Hz. This property can be set.
        """
    )
    stop_frequency = Instrument.control(
        ":SENS:FREQ:STOP?", ":SENS:FREQ:STOP %e",
        """ A floating point property that represents the stop frequency
        in Hz. This property can be set.
        """
    )
    # frequency_points = Instrument.control(
    #     ":SENSe:SWEEp:POINts?", ":SENSe:SWEEp:POINts %d",
    #     """ An integer property that represents the number of frequency
    #     points in the sweep. This property can take values from 101 to 3001.
    #     """,
    #     validator=truncated_range,
    #     values=[101, 3001],
    #     cast=int
    # )
    frequency_step = Instrument.control(
        ":SENS:FREQ:CENT:STEP:INCR?", ":SENS:FREQ:CENT:STEP:INCR %g",
        """ A floating point property that represents the frequency step
        in Hz. This property can be set.
        """
    )
    center_frequency = Instrument.control(
        ":SENS:FREQ:CENT?", ":SENS:FREQ:CENT %e",
        """ A floating point property that represents the center frequency
        in Hz. This property can be set.
        """
    )
    sweep_time = Instrument.control(
        ":SENS:SWE:TIME?", ":SENS:SWE:TIME %.2e",
        """ A floating point property that represents the sweep time
        in seconds. This property can be set.
        """
    )

    def __init__(self, adapter, name="Rigol DSA815 Spectrum Analyzer", **kwargs):
        super().__init__(
            adapter,
            name,
            **kwargs
        )

    @property
    def frequencies(self):
        """ Returns a numpy array of frequencies in Hz that
        correspond to the current settings of the instrument.
        """
        return np.linspace(
            self.start_frequency,
            self.stop_frequency,
            self.frequency_points,
            dtype=np.float64
        )

    def trace(self, number=1):
        """ Returns a numpy array of the data for a particular trace
        based on the trace number (1, 2, or 3).
        """(":FORMat:TRACe:DATA ASCII")
        data = np.loadtxt(
            StringIO(self.ask(":TRACE:DATA? TRACE%d" % number)),
            delimiter=',',
            dtype=np.float64
        )
        return data

        self.write
    def trace_df(self, number=1):
        """ Returns a pandas DataFrame containing the frequency
        and peak data for a particular trace, based on the
        trace number (1, 2, or 3).
        """
        return pd.DataFrame({
            'Frequency (GHz)': self.frequencies * 1e-9,
            'Peak (dB)': self.trace(number)
        })
