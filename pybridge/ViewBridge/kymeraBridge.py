from ophyd import Device, Component as Cpt, PVPositioner
from ophyd import Signal, SignalRO
from pylablib.devices import Andor



class AndorIDUSViewerBridge(Device):
    timeout = Cpt(Signal, value=5)
    exposure_time = Cpt(Signal, value = 1)
    image = Cpt(SignalRO, value=None)
    read_mode = Cpt(Signal, value="fvb")


    def __init__(
            self,
            prefix="",
            *,
            name,
            parent=None, kind=None,
            **kwargs,
    ):
        super().__init__(name=name, parent=parent, kind=kind, **kwargs)
        self.device = Andor.AndorSDK2Camera()
        self.connect()
        self.exposure_time.put = self.set_exposure
        self.exposure_time.get = self.get_exposure
        self.image.get = self.get_single_image
        self.read_mode.put = self.set_read_mode
        self.read_mode.get = self.get_read_mode

    

    def connect(self):
        if not self.device.is_opened():
            self.device.open()
        elif self.device.is_opened():
            return True
        else:
            raise ConnectionError("Andor IDus cannot connect. Retry again.") 
    def get_device_info(self):
        if self.device.is_opened():
            return self.device.get_device_info()
        else:
            raise RuntimeError("Device is not connected. Please connect first.")
        
    def disconnect(self):
        if self.device.is_opened():
            self.device.close()
        else:
            pass
    
    def get_images(self, num_frame = 1):
        self.device.start_acquisition()
        self.device.wait_for_frame()
        image = self.device.grab(nframes= num_frame, frame_timeout=self.timeout.get())
        if image is not None:
            return image 
        else:
            raise RuntimeError("Failed to retrieve image. Ensure the camera is properly configured and connected.")
    
    def get_single_image(self):
        """Retrieve a single image from the camera.
        Returns:
            numpy.ndarray: The captured image.
        Raises:
            RuntimeError: If the camera is not connected or if image retrieval fails.
        """
        self.device.start_acquisition()
        self.device.wait_for_frame()
        image = self.device.snap(timeout = self.timeout.get())
        return image

    def get_exposure(self):
        """Retrieve the current exposure time of the camera.
        Returns:
            float: The exposure time in seconds. 
        """
        return self.device.get_exposure()
    
    def set_exposure(self, exp_time):
        """Set the exposure time of the camera.
        Args:
            exp_time (float): The exposure time in seconds.
        Raises:
            ValueError: If the exposure time is not a positive number.
        """
        if exp_time <= 0:
            raise ValueError("Exposure time must be greater than zero.")
        self.device.set_exposure(exp_time)
    
    def set_timeout(self, timeout):
        """Set the timeout for the camera
        Args:
            timeout (float): The timeout in seconds.
        Raises:
            ValueError: If the timeout is not a positive number.
        """
        if timeout <= 0:
            raise ValueError("Timeout must be greater than zero.")
        self.timeout.put(timeout)
    def get_timeout(self):
        """Retrieve the current timeout setting of the camera.
        Returns:
            float: The timeout in seconds.
        """
        return self.timeout.get()

    def set_read_mode(self, mode):
        """Set the read mode of the camera. 
        Args:
            mode (str): The read mode to set. Valid options are 'normal', 'fast', etc.
        Raises:
            ValueError: If the mode is not recognized.
        """
        valid_modes = ["fvb", "single_track", "multi_track", "random_track", "image"]
        if mode not in valid_modes:
            raise ValueError(f"Invalid read mode. Valid options are: {', '.join(valid_modes)}")
        self.device.set_read_mode(mode)
    
    def get_read_mode(self):
        """Retrieve the current read mode of the camera.
        Returns:
            str: The current read mode.
        """
        return self.device.get_read_mode()