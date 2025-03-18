from MoveBridge.hardware_interface import SHRCStage
from bluesky import RunEngine

class SHRCProcedure(): 
    
    ch= SHRCStage('COM3', name = 'SHRC', settle_time = 5)
    # stage = {'X': ch.X, 'Y': ch.Y, 'Z': ch.Z}
    
    def prepare_stage(self):
        self.ch.home()
        self.ch.speed_initial(1, self.ch.X)
        self.ch.speed_initial(1, self.ch.Y)
        self.ch.speed_initial(1, self.ch.Z)
        self.ch.accel_time(1, self.ch.X)
        self.ch.accel_time(1, self.ch.Y)
        self.ch.accel_time(1, self.ch.Z)
    
    def move_stage(self, position):
        self.ch.move(position, self.ch.X)
        self.ch.move(position, self.ch.Y)
        self.ch.move(position, self.ch.Z)

    def close(self):
        self.ch.close_connection()
    
if __name__ == "__main__":
    RE = RunEngine({})
    shrc = SHRCProcedure()
    shrc.prepare_stage()
    shrc.move_stage(10)
    shrc.close()
