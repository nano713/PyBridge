# Zaber visaDriver to control the actuator (we can change it later)


from zaber_motion.ascii import Connection
from zaber_motion import Units, Tools
from zaber_motion.exceptions.connection_failed_exception import ConnectionFailedException
import logging

logger = logging.getLogger(__name__)

class ZaberConnection: 
    """Class to connect the Zaber Actuators"""

    def __init__(self, port, axis_index): 
        self.axis_index = axis_index
        self.device_list = Connection.open_serial_port(port_name=port).detect_devices
        if len(self.device_list) == 0:
            return logger.critical("Device list has none")
    
    def open_connection(self):
        for i, device in enumerate(self.device_list):
            i += 1
            axis_control = device.get_axis(self.axis_index)
            