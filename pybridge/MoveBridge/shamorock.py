from pylablib.devices import Andor
from ophyd import Device, Component as Cpt, PVPositioner
from ophyd import Signal, SignalRO




class SpectroGraphMoveBridge(PVPositioner):
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
        return self.spectrographs
    
    def set_grating(self, grate):
        if isinstance(grate, int):
            self.spectrographs[grate - 1].set_grating(grate)
            self.spectrograph.put(grate)
        else:
            raise ValueError("Grate is not an int. Modify numerical value")
    
    def get_grating(self):
        index = self.spectrograph.get()
        return self.spectrographs[index - 1].get_grating()
    
    def set_center_wavelength(self, fequency):
       index = self.spectrograph.get()
       self.spectrographs[index - 1].set_wavelength(fequency)

    def get_center_wavelength(self):
        index = self.spectrograph.get()
        wavelength = self.spectrographs[index - 1].get_wavelength()
        wavelength = wavelength * 1e9 #convert to nm
        return wavelength
"""
# Connection
>> from pylablib.devices import Andor
>> Andor.list_shamrock_spectrographs()
["KY-1234"]
>> spec = Andor.ShamrockSpectrograph(idx=0)
>> spec.close()

# Operation
>> from pylablib.devices import Andor
>> cam = Andor.AndorSDK2Camera()  # camera should be connected first
>> spec = Andor.ShamrockSpectrograph()
>> spec.set_wavelength(600E-9)  # set 600nm center wavelength
>> spec.setup_pixels_from_camera(cam)  # setup camera sensor parameters (number and size of pixels) for wavelength calibration
>> wavelengths = spec.get_calibration()  # return array of wavelength corresponding to each pixel
>> cam.set_image_mode("fvb")
>> spectrum = cam.snap()[0]  # 1D array of the corresponding spectrum intensities
>> cam.close()
>> spec.close()

- get/set center wavelength
- get/set grating
"""

