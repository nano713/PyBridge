from ophyd import Device, Component as Cpt, PVPositioner
from ophyd import Signal, SignalRO
from pylablib.devices import Andor



class AndorIDUSViewerBridge(Device):

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
    

    def connect(self):
        if not self.device.is_opened():
            self.device.open()
        else:
            pass 
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
        image = self.device.grab(nframes= num_frame)
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
        image = self.device.snap(timeout = 5)
        