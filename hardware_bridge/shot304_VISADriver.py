#microscope hardware
import pyvisa
import pyvisa.constants # DK - this is included in `import pyvisa`

class SHOT304VISADriver:
    def __init__(self, com):
        self.shot304 = None
        self.rsrc_name = com
    
    def open_connection(self): 
        """Opens a connection with the microscope."""
        self.shot304 = pyvisa.ResourceManager().open_resource(self.rsrc_name) # "ASRL3::INSTR"
        self.shot304.baud_rate = 38400
        self.shot304.data_bits = 8
        self.shot304.parity = pyvisa.constants.Parity.none
        self.shot304.stop_bits = pyvisa.constants.StopBits.one
        self.shot304.write_termination = "\r\n"
        self.shot304.read_termination = "\r\n"
        self.shot304.flow_control.rts_cts = True #check documentation if true or false
        self.shot304.timeout = 5000
    
    def move(self, position, axis): 
        """"Moves the microscope to a specific position.
            Inputs: 
                position: int, position to move to
                axis: int, axis number
            Returns:
                None"""
        if position > 0:
            self.shot304.query(f"A:{axis}+P{position}")
        else: 
            self.shot304.query(f"A:{axis}-P{abs(position)}")
        self.shot304.query("G:")
    
    def get_position(self, axis):
        """"Returns the current position of the microscope.
            Inputs:
                axis: int, axis number
            Returns:
                position: int, current position"""
        position = self.shot304.query(f"Q:")   
        if position is not None: 
            position = position.split(",")[axis-1].strip()
        return position
    
    def set_speed(self, speed_ini=1000, speed_fin=10000, acc=100, axis=1):
        """"Sets the speed and acceleration of the microscope.
            Inputs: 
                speed_ini: int, initial speed
                speed_fin: int, final speed
                acc: int, acceleration
                axis: int, axis number
            Returns:
                None""" 
        if 0 < speed_ini < 500000 and 0 < speed_fin < 500000 and 0 < acc < 1000:
            self.shot304.query(f"D:{axis}S{speed_ini}F{speed_fin}R{acc}")
        else: 
            raise ValueError("Speed and acceleration values must be between 0 and 500000 and 0 and 1000, respectively.")
    
    def get_speed(self, axis): 
        """"Returns the speed and acceleration of the microscope.
            Inputs: 
                axis: int, axis number
            Returns:
                speed_ini: int, initial speed
                speed_fin: int, final speed
                acc: int, acceleration"""
        speed = self.shot304.query(f"?:D{axis}")
        if speed is not None:
            speed_ini = speed.split("S")[1].split("F")[0]
            speed_fin = speed.split("F")[1].split("R")[0]
            acc = speed.split("R")[1]
        return speed_ini, speed_fin, acc
    
    def get_status(self): 
        status = self.shot304.query("!:")
        if status == "R":
            return True
        else:
            return False

    def home(self, axis): 
        """Returns the miscroscope to mechanical home position.
            Inputs: 
                axis: int, axis number
            Returns: 
                None"""
        self.shot304.query(f"H:{axis}")
    
    def stop(self, axis):
        """"Stops the motion of the microscope.
            Inputs: 
                axis: int, axis number
            Returns: 
                None"""
        self.shot304.query(f"L:{axis}")
    
    def close_connection(self):
        """Closes the connection with the microscope."""
        self.shot304.close()

    # Can we add a method to change the mode into remote (: host) mode?