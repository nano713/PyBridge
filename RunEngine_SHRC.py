from hardware_interface import SHRCStage
from bluesky import RunEngine

class SHRCProcedure(): 
    RE = RunEngine({})
    ch= SHRCStage('COM3')
    stage = {'X': ch.X, 'Y': ch.Y, 'Z': ch.Z}
    
    def prepare_stage(self):
        self.ch.home()
        self.ch.set_velocity(1, self.ch.X)
        self.ch.set_velocity(1, self.ch.Y)
        self.ch.set_velocity(1, self.ch.Z)
        self.ch.set_acceleration(1, self.ch.X)
        self.ch.set_acceleration(1, self.ch.Y)
        self.ch.set_acceleration(1, self.ch.Z)
    
    def move_stage(self, position):
        self.ch.move(position, self.ch.X)
        self.ch.move(position, self.ch.Y)
        self.ch.move(position, self.ch.Z)

    def close(self):
        self.ch.close_connection()
    
if __name__ == "__main__":
    shrc = SHRCProcedure()
    shrc.prepare_stage()
    shrc.move_stage(10)
    shrc.close()