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
"""