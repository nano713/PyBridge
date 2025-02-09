from hardware_interface import SHRCStage
from bluesky import RunEngine

class SHRCProcedure(): 

    def run_engine():
        
        RE = RunEngine({})
        ch= SHRCStage('COM3')
        stage = {'X': ch.X, 'Y': ch.Y, 'Z': ch.Z}
        return 