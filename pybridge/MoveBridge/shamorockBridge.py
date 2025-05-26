from pylablib.devices import Andor
from ophyd import Device, Component as Cpt, PVPositioner
from ophyd import Signal, SignalRO

class SpectroGraphMoveBridge(PVPositioner):
    """Class that controls the """
    spectrograph = Cpt(Signal, value=1, kind="config") #gets the current grating
    setpoint = Cpt(Signal) #target position
    readback = Cpt(SignalRO) #Read position
    done = Cpt(Signal, value = False) #Instrument is done moving
    actuate = Cpt(Signal) #Request to move
    stop_signal =  Cpt(Signal) #Request to stop

    
    def __init__(
        self,
        prefix="",
        *,
        limits=None,
        name=None,
        read_attrs=None,
        configuration_attrs=None,
        parent=None,
        egu="",
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
        self.spectrographs = []
        self.connect()
        self.readback.get = self.get_center_wavelength
        self.setpoint.put = self.set_grating
    
    def connect(self):
        """Connect to the Andor Shamrock spectrograph.
        This method initializes the connection to the Andor Shamrock spectrograph.
        """
        list = Andor.list_shamrock_spectrographs()
        list_length = len(list)
        if list_length == 0:
            raise RuntimeError("No Shamrock spectrograph found.")
        elif list_length > 1:
            for i in range(list_length):
                print(f"{i}: {list[i]}")
                andor_com = Andor.ShamrockSpectrograph(idx = i)
                self.spectrographs.append(andor_com)
        else:
            print(f"0: {list[0]}")
            andor_com = Andor.ShamrockSpectrograph(idx = 0)
            self.spectrographs.append(andor_com)
    
    def get_spectrographs(self):
        """Get the list of connected spectrographs.
        Returns:
            list: List of connected spectrographs.
        """
        return self.spectrographs
    
    def set_grating(self, grate):
        """Set the grating of the current spectrograph.
        Args:
            grate (int): The grating number to set.
            Raises:
                ValueError: If the grate is not an integer.
        """
        if isinstance(grate, int):
            self.spectrographs[grate - 1].set_grating(grate)
            self.spectrograph.put(grate)
        else:
            raise ValueError("Grate is not an int. Modify numerical value")
    
    def get_grating(self):
        """Get the grating of the current spectrograph.
        Returns:
            int: The grating number of the current spectrograph.
        """
        index = self.spectrograph.get()
        return self.spectrographs[index - 1].get_grating()
    
    def set_center_wavelength(self, frequency):
        """Set the center wavelength of the current spectrograph.
         Args:
            frequency (float): The center wavelength in nm to set.
        Raises:
            ValueError: If the frequency is not a float.
        """
        index = self.spectrograph.get()     
        if isinstance(frequency, float):
            if self.get_wavelength_limits()[0] <= frequency <= self.get_wavelength_limits()[1]:
                self.spectrographs[index - 1].set_wavelength(frequency)
            
            elif frequency  < self.get_wavelength_limits()[0]:
                frequency = self.get_wavelength_limits()[0]
                self.spectrographs[index - 1].set_wavelength(frequency)

            elif frequency > self.get_wavelength_limits()[1]:
                frequency = self.get_wavelength_limits()[1]
                self.spectrographs[index - 1].set_wavelength(frequency)
            
            else:
                raise ValueError("Frequency is not in the wavelength limits. Modify numerical value")
        else:
            raise ValueError("Frequency is not a float. Modify numerical value")
    def get_center_wavelength(self):
        """Get the center wavelength of the current spectrograph.
        Returns:
            float: The center wavelength in nm of the current spectrograph.
        """
        index = self.spectrograph.get()
        wavelength = self.spectrographs[index - 1].get_wavelength()
        wavelength = wavelength * 1e9 #convert to nm
        return wavelength
    
    def get_wavelength_limits(self):
        """"Get the wavelength limits of the current spectrograph.
        Returns:
            tuple: (lower_limit, upper_limit) in nm
        """
        index = self.spectrograph.get()
        limits = self.spectrographs[index - 1].get_wavelength_limits()
        limits = [limit * 1e9 for limit in limits]
        lower_limit = limits[0]
        upper_limit = limits[1]
        return lower_limit, upper_limit
    
    def close(self):
        """"Close all spectrographs.
        This method should be called when the spectrograph is no longer needed.
        """
        for spectrograph in self.spectrographs:
            self.spectrographs.close()
        self.spectrographs = []
    
    def get_settings(self):
        """Get the settings of the current spectrograph.
        Returns:
            dict: Dictionary containing the settings of the spectrograph.
        """
        index = self.spectrograph.get()
        settings = self.spectrographs[index - 1].get_settings()
        return settings