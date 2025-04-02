from zaber_motion.ascii import Connection
from zaber_motion import Units, Tools
from zaber_motion.exceptions.connection_failed_exception import ConnectionFailedException
import logging

logger = logging.getLogger(__name__)
from ophyd import PVPositioner, Signal, SignalRO, Component as Cpt, Device
from ophyd.status import MoveStatus

class ZaberConnect:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ZaberConnect, cls).__new__(cls, *args, **kwargs)
        return cls._instance
    
    def __init__(self):
        self.controller = []
        self.controller_axis = []
        self.unit = []
        self.unit_object = None
        self.stage_type = []
        if not hasattr(self, 'initialized'):
            self.initialized = True
            self.zaber = None
            ports = Tools.list_serial_ports()
            if len(ports) == 0:
                print("No Zaber devices found.")
                return
            for port in ports:
                if port == "COM5":
                    self.connect(port = port)
                    # try:
                    #     # self.port = "COM5" 
                    #     self.connect(port = "COM5")
                    # except:
                    #     logger.error(f"Could not connect to Zaber device via {port}")
                    #     return  
    
    def connect(self, port):
        """Connect to the Zaber controller"""
        connection = Connection.open_serial_port(port)
        device_list = connection.detect_devices()
        if len(device_list) == 0:
            logger.error("No devices found")
        self.zaber = connection

        for i, device in enumerate(device_list):
            i += 1
            # self.controller.append(device)
            axis_control = device.get_axis(1)
            self.controller_axis.append(axis_control)
            axis_type = str(axis_control.axis_type).replace("AxisType.", "")
            self.stage_type.append(axis_type)
            self.unit.append('')
            if axis_control.axis_type.value == 1:
                self.units_update('um', i)
            elif axis_control.axis_type.value == 2: 
                self.units_update('degree', i)
        logger.info(f"Connected to {len(device_list)} devices")
    
    def move_abs(self, position, axis): 
        if (axis > 0):
            axes = self.controller_axis[axis-1]        
            axes.move_absolute(position, self.unit[axis-1])
        else:
            logger.error("Axis is not a valid integer")
    
    def move_relative(self, position, axis):
        """Move the stage relative to its current position
        Args:
            position (float): The distance to move the stage in the unit of the stage.
            axis (int): The axis number to move.
        """
        if (axis > 0): 
            axes = self.controller_axis[axis-1]
            axes.move_relative(position, self.unit[axis-1])
        else:
            logger.error("Axis is not a valid integer")
    def get_position(self, axis, unit):
        """Get the current position of the stage in the unit of the stage.
        Args:
            axis (int): The axis number to get the position.
        Returns:
            float: The current position of the stage in the unit of the stage.
            """ 
        if (axis > 0):
            axes = self.controller_axis[axis-1]
            unit = self.units_update(unit, axis)
            return axes.get_position(unit) #TODO: FIX THIS AND THE AXES
        else:
            logger.error("Axis is not a valid integer")
    def home(self, axis):
        """Home the stage.
        Args:
            axis (int): The axis number to home.
        """
        if (axis > 0): 
            axes = self.controller_axis[axis-1]
            axes.home()
        else:
            logger.error("Controller is not a valid integer")
    def stop(self, axis):
        """Stop the stage.
        Args:
            axis (int): The axis number to stop.
        """
        if (axis > 0): 
            axes = self.controller_axis[axis-1]
            axes.stop()
        else:
            logger.error("Controller is not a valid integer")
    
    def stage_name(self,axis):
        """Get the stage name.
        Args:
            axis (int): The axis number to get the stage name.
        Returns:
            str: The stage name.
        """
        return self.stage_type[axis-1]

    def units_update(self, unit, axis):
        """Update the unit of the stage. 
        Args:
            unit (str): The unit of the stage.
            axis (int): The axis number to update the unit.
        """
        if unit == "um":
            self.unit_object = Units.LENGTH_MICROMETRES
            Units.LENGTH_MICROMETRES
        elif unit == "degree":
            self.unit_object = Units.ANGLE_DEGREES
            Units.ANGLE_DEGREES
        elif unit == "rad":
            self.unit_object = Units.ANGLE_RADIANS
            Units.ANGLE_RADIANS

        self.unit[axis-1] = unit
        return self.unit_object


class ZaberStage(PVPositioner):
    setpoint = Cpt(Signal) #target position
    readback = Cpt(SignalRO) #Read position
    done = Cpt(Signal, value = False) #Instrument is done moving
    actuate = Cpt(Signal) #Request to move
    stop_signal =  Cpt(Signal) #Request to stop


    axis_index = Cpt(Signal, value=1, kind="config") 
    unit = Cpt(Signal, value="um", kind="config")

    def __init__(
            self,
            prefix="",
            *,
            limits=None,
            name=None,
            read_attrs=None,
            configuration_attrs=None,
            parent=None,
            egu="um",
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
        self.zaber = ZaberConnect()
        self.axis_list = self.zaber.controller_axis
        self.unit_list = self.zaber.unit
        self.readback.get = self.get_position
        
        index = 0
        while index < len(self.axis_list):
            self.axis_index.put(index + 1)
            self.unit.put(self.unit_list[index])
            index += 1
    def move(self, position: float, wait=True, timeout=None):
        """Move the stage to the absolute position.
        Args:
            position (float): The absolute position to move the stage to.
        """
        value = self.zaber.move_abs(position, self.axis_index.get())
        self.setpoint.put(position)
        status = MoveStatus(self, target = position, timeout = timeout, settle_time = self._settle_time)
        if value == 1:
            self.done.put(True)
        else:
            self.done.put(False)
        status.set_finished()
        return status

    def move_relative(self, position): 
        """Move the stage relative to its current position.
        Args:
            position (float): The distance to move the stage in the unit of the stage.
        """
        self.zaber.move_relative(position, self.axis_index.get())
    def get_position(self):
        """Get the current position of the stage in the unit of the stage.
        Returns:
            float: The current position of the stage in the unit of the stage.
        """
        self.unit.put(self.unit_list[self.axis_index.get() -1])
        print(self.unit.get())
        print(self.axis_index.get())
        return self.zaber.get_position(self.axis_index.get(), self.unit.get())
    def stop(self, *, success: bool = False):
        """Stop the stage.
        """
        if self.stop_signal is not None:
            self.stop_signal.put(value = self.stop_value) 
        self.zaber.stop(self.axis_index.get())
    def home(self):
        """Home the stage.
        """
        self.zaber.home(self.axis_index.get())
        self.setpoint.put(self.get_position())

    def get_axis(self):
        """Get the axis number.
        Returns:
            int: The axis number.
        """
        return self.axis_index.get()