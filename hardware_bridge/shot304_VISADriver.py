#microscope hardware
import pyvisa 

class SHOT304VISADriver:
    def __init__(self, com):
        self.shot304 = None
        self.rsrc_name = com
    
    def open_connection(self): 
        self.shot304 = pyvisa.ResourceManager().open_resource(self.rsrc_name)
        self._instr.baud_rate = 38400
        self._instr.data_bits = 8 
        self._instr.parity = pyvisa.constants.Parity.none 
        self._instr.write_termination = "\r\n" 
        self._instr.read_termination = "\r\n"
        self._instr.flow_control.rts_cts = True
        self._instr.timeout = 50000
    
    def move(self, position, axis): 
        if position > 0:
            self.shot304.write(f"A:{axis}+{position}")
        else: 
            self.shot304.write(f"A:{axis}-{abs(position)}")
        self.shot304.write("G:")

    def home(self): 
        self.shot304.write("H:")
    
    def stop(self):
        self.shot304.write("L: E")
    
    def close_connection(self):
        self.shot304.close()