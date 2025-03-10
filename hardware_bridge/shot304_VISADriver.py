#microscope hardware
import pyvisa
import pyvisa.constants # DK - this is included in `import pyvisa`

class SHOT304VISADriver:
    def __init__(self, com):
        self.shot304 = None
        self.rsrc_name = com
    
    def open_connection(self): 
        self.shot304 = pyvisa.ResourceManager().open_resource(self.rsrc_name) # "ASRL3::INSTR"
        self.shot304.baud_rate = 38400
        self.shot304.data_bits = 8
        self.shot304.parity = pyvisa.constants.Parity.none
        self.shot304.stop_bits = pyvisa.constants.StopBits.one
        self.shot304.write_termination = "\r\n"
        self.shot304.read_termination = "\r\n"
        self.shot304.flow_control.rts_cts = True #check documentation if true or false
        self.shot304.timeout = 5000
    
    def move(self, position, axis): # DK - Check with the manual if this command is correct.
        if position > 0:
            self.shot304.write(f"A:{axis}+{position}")
        else: 
            self.shot304.write(f"A:{axis}-{abs(position)}")
        self.shot304.write("G:")
    
    def get_position(self): # DK - extract the position from strings '        10,   1000000,         0,         0,K,K,R'
        return self.shot304.query(f"Q:")
    
    def set_speed(self, speed_ini, speed_fin, acc, axis): 
        if 0 < speed_ini < 500000 and 0 < speed_fin < 500000 and 0 < acc < 1000:
            self.shot304.write(f"D:{axis}S{speed_ini}F{speed_fin}R{acc}")
        else: 
            raise ValueError("Speed and acceleration values must be between 0 and 500000 and 0 and 1000, respectively.")

    def home(self): 
        # DK - you need to specify the axis
        self.shot304.write("H:")
    
    def stop(self):
        # DK - it seems that L:E is an emergency stop. If this is normal stop, we should use a command that decelerates and stops.
        self.shot304.write("L:E")
    
    def close_connection(self):
        self.shot304.close()

    # Can we add a method to change the mode into remote (: host) mode?