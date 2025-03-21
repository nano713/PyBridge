# 

from zaber_motion.ascii import Connection
from zaber_motion import Units, Tools
from zaber_motion.exceptions.connection_failed_exception import ConnectionFailedException
import logging 

logger = logging.getLogger(__name__)

class ZaberConnection: 
    def __init__(self, port, axis, type):
        self.axis_index = axis
        self.device_list = []
        if type == 'Linear': 
            self.unit = Units.LENGTH_MICROMETERS
            self.value = 1
        elif type == 'Rotation':
            self.unit = Units.ANGLE_DEGREES
            self.value = 2
        else:
            logger.critical("Invalid type")
        try:
            self.device_list = Connection.open_serial_port(port).detect_devices()
            if len(self.device_list) == 0:
                logger.critical("No devices found")
            self.axis_control = self.device_list[self.axis_index].get_axis(self.value)
        except ConnectionFailedException:
            logger.critical("Connection failed")
    
    def move_abs(self, position): 
        if (self.axis_index > 0): 
            self.axis_control.move_absolute(position, self.unit)
        else:
            logger.error("Axis is not a valid integer")
    
    def move_relative(self, position): 
        if (self.axis_index > 0): 
            self.axis_control.move_relative(position, self.unit)
        else:
            logger.error("Axis is not a valid integer")
    
    def get_position(self):
        if (self.axis_index > 0): 
            return self.axis_control.get_position()
    
    def home(self): 
        if (self.axis_index > 0): 
            self.axis_control.home()
        else:
            logger.error("Axis is not a valid integer")
    
    def stop(self): 
        if (self.axis_index > 0): 
            self.axis_control.stop()
        else:
            logger.error("Axis is not a valid integer")
    
    def get_axis_type(self):
        #Check if this axis command works or not
        return self.axis_control.axis_type.value


        