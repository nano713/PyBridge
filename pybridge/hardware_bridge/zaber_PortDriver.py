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
    def __init__(self, port, axis): 
        self.axis_index = axis 
        self.device_list = []

        try:
            self.device_list = Connection.open_serial_port(port).detect_devices()
            if len(self.device_list) == 0:
                logger.critical("No devices found")
            self.axis_control = self.device_list[self.axis_index].get_axis(1) 
        except ConnectionFailedException:
            logger.critical("Connection failed") 

    def open_stage(self): 
        """Opens the stage and sets the unit based on the instrument """  
        AXXXXIS_TYPE = self.axis_control.axis_type

        if "LINEAR" in str(AXXXXIS_TYPE):
            self.unit = Units.LENGTH_MICROMETRES 
        elif "ROTARY" in str(AXXXXIS_TYPE):
            self.unit = Units.ANGLE_DEGREES
        else:
            logger.critical("Invalid type")

    def move_abs(self, position): 
        """Moves the stage to the absolute position based on the axis index.
        Args: 
            position (int): The position to move to.
"""
        if (self.axis_index > 0):
            self.axis_control.move_absolute(position, self.unit)
        else:
            logger.error("Axis is not a valid integer")
    
    def move_relative(self, position): 
        """Moves the stage to the relative position based on the axis index.
        Args: 
            position (int): The position to move to.
        """
        if (self.axis_index > 0): 
            self.axis_control.move_relative(position, self.unit)
        else:
            logger.error("Axis is not a valid integer")
    
    def get_position(self):
        """Gets the position of the stage based on the axis index.
        Returns: 
            int: The position of the stage.
        """
        if (self.axis_index > 0): 
            return self.axis_control.get_position(self.unit)
    
    def home(self):
        """Homes the stage based on the axis index.""" 
        if (self.axis_index > 0): 
            self.axis_control.home()
        else:
            logger.error("Axis is not a valid integer")
    
    def stop(self): 
        """Stops the stage based on the axis index."""
        if (self.axis_index > 0): 
            self.axis_control.stop()
        else:
            logger.error("Axis is not a valid integer")
    
    def get_axis_type(self):
        """Gets the axis type of the stage based on the axis index.
        Returns: 
            str: The axis type of the stage.
        """
        return self.axis_control.axis_type.value 
        