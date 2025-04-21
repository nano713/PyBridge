#microscope hardware
import pyvisa
import pyvisa.constants # DK - this is included in `import pyvisa`
import time

class SHOT304VISADriver:
    def __init__(self, com):
        self.shot304 = None
        self.rsrc_name = com
        self.um2pulse = 100

        self.open_connection()
        self.set_speed(10000, 100000, 100, 1)
        self.set_speed(10000, 100000, 100, 2)
        self.set_speed(10000, 100000, 100, 3)
        # self.home(1)
        # self.home(2)
        # self.home(3)
    
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
        pulse = int(position * self.um2pulse)
        if position > 0:
            self.shot304.query(f"A:{axis}+P{pulse}")
        else: 
            self.shot304.query(f"A:{axis}-P{abs(pulse)}")
        self.shot304.query("G:")
        # self.wait_for_ready()

    def move_relative(self, position, axis):
        pulse = int(position*self.um2pulse)
        if pulse > 0 :
            self.shot304.query(f"M:{axis}+P{pulse}")
        else:
          self.shot304.query(f"M:{axis}-P{abs(pulse)}")
        self.shot304.query("G:")  
        # self.wait_for_ready()

    def get_position(self, axis):
        """"Returns the current position of the microscope.
            Inputs:
                axis: int, axis number
            Returns:
                position: int, current position"""
        
        pulse = self.shot304.query(f"Q:")
        if pulse is not None: 
            pulse = pulse.split(",")[axis-1].strip()
            is_negative = pulse.startswith('-')
            pulse = ''.join(filter(str.isdigit, pulse))
            if is_negative:
                pulse = f"-{pulse}"
            pulse = int(pulse)
            position = pulse / self.um2pulse
        return position
    
    def set_speed(self, speed_ini=10000, speed_fin=100000, acc=100, axis=1):
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
            
        return int(speed_ini), int(speed_fin), int(acc)
    
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
        self.move(0, axis)
        
        self.shot304.query(f"H:{axis}")
        self.shot304.query("G:")
    
    def stop(self, axis):
        """"Stops the motion of the microscope.
            Inputs: 
                axis: int, axis number
            Returns: 
                None"""
        self.shot304.query(f"L:{axis}")
    
    def wait_for_ready(self, timeout=20):
        """Waits for the microscope to be ready."""
        time0 = time.time()
        while not self.get_status():
            time.sleep(0.1)
            if time.time() - time0 >= timeout:
                raise TimeoutError("Timeout waiting for the microscope to be ready.")
        return True

    def close_connection(self):
        """Closes the connection with the microscope."""
        self.shot304.close()

    # Can we add a method to change the mode into remote (: host) mode?