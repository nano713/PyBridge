# 

from zaber_motion.ascii import Connection
from zaber_motion import Units, Tools
from zaber_motion.exceptions.connection_failed_exception import ConnectionFailedException
import logging 

logger = logging.getLogger(__name__)

class ZaberConnection: 
    """...

    Attributes
    ----------
    ...
    self.value : int
        The value of the axis. <- index of the axis 
    ...
    """
    def __init__(self, port, axis): # The attribute should be only port and axis. Use zaber_motion's axis_type method to get `type`. I suggest __init__(self, port, axis_index)
        self.axis_index = axis # I prefer to use the term axis_index instead of axis because it is an integer value.
        self.device_list = []

        try:
            self.device_list = Connection.open_serial_port(port).detect_devices()
            if len(self.device_list) == 0:
                logger.critical("No devices found")
            self.axis_control = self.device_list[self.axis_index].get_axis(1) # DK - I suggest .get_axis(self.axis_index) because this axis index can be other than 1 or 2.
        except ConnectionFailedException:
            logger.critical("Connection failed") 
    


    def open_stage(self):   
        AXXXXIS_TYPE = self.axis_control.axis_type

        if "LINEAR" in str(AXXXXIS_TYPE):
            self.unit = Units.LENGTH_MICROMETRES 
        elif "ROTARY" in str(AXXXXIS_TYPE):
            self.unit = Units.ANGLE_DEGREES
        else:
            logger.critical("Invalid type")


    def move_abs(self, position): 
        if (self.axis_index > 0): # DK - since axis_index is not an attribute, I suggest `if axis object: to check if axis object exists. Applicable to methods below, too.
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
            return self.axis_control.get_position(self.unit)
    
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
        return self.axis_control.axis_type.value # DK - axis object has axis_type method. Do we need to call the method from axis_control?


        