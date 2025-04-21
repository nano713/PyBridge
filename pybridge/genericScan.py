from bluesky import RunEngine
from ophyd import Signal, SignalRO
from bluesky.plans import scan
from bluesky.plans import grid_scan
from bluesky.plans import count
from ophyd.sim import motor1, motor2, motor3, det1, det2, det3, det4
from bluesky.callbacks.best_effort import BestEffortCallback

class GenericScan:
    def __init__(self, name_scan, array, detectors):
        self.RE = RunEngine()
        self.motor = []
        self.dets = []
        self.create_instance(detectors)
        self.array_scan = array
        self.has_attribites(name_scan)
    
    def create_instance(self, detectors):
        for i in range(len(detectors)):
            detector = detectors[i]
            detector = detector(name = "Daichi is annoying")
            self.dets.append(detector)

    def has_attribites(self, name_scan):
        """Check if the class is either MoveBridge or ViewerBridge.
        If not, raise an error.
        Args:
            name_scan: The class to check.
        """
        try:
            class_string = str(name_scan)
        except Exception as e:
            raise ValueError(f"Error in class name: {e}")

        if "MoveBridge" in class_string:
            print("MoveBridge")
        elif "ViewerBridge" in class_string:
            print("ViewerBridge")
        else:
            raise ValueError(f"Unknown scan type: {name_scan}")
    
    def run_move(self, class_name):
        bec = BestEffortCallback()

        self.RE.subscribe(bec)  
                
        class_done = class_name(name = "test")
        grid_scan_args = []
        print("Error passed")
        for i, scan in enumerate(self.array_scan): 
            motor = scan[0]
            if motor == class_name:
                motor = class_done
            elif motor is None:
                motor = motor(name = "Daichi is the dummy one :)")
            start,stop,step = scan[1:]
            grid_scan_args.append(motor)
            grid_scan_args.append(start)
            grid_scan_args.append(stop)
            grid_scan_args.append(step)
 
        print("self.dets,*grid_scan_args =", self.dets,*grid_scan_args)
        self.RE(grid_scan(self.dets,*grid_scan_args)) # Extends the grid scan with dynamic motor and scan values

         

    # def run_viewer(self, class_name):
    #     class_done = class_name(name = "daichi doesn't know when to stop and listen at times")
    #     scan = []
    #     for i, scan in enumerate(self.array_scan):
    #         motor = scan[0]
    #         if motor == class_name:


if __name__ == "__main__":
    from ophyd.sim import motor1, motor2, motor3, det1, det2, det3, det4
    from pybridge.MoveBridge.shrcBridge import SHRCMoveBridge
    from pybridge.ViewBridge.interface_Keithely2100 import Keithley2100ViewerBridge
    from pybridge.genericScan import GenericScan
    # Example usage
    
    class_name = SHRCMoveBridge # or "ViewerBridge"
    shrc = SHRCMoveBridge(name="shrc")

    # scan = GenericScan(class_name, array_scan)
    # gene = GenericScan(SHRCMoveBridge,[[motor1, 1, 10, 10], [motor2, 1, 10, 10]], [Keithley2100ViewerBridge])
    gene = GenericScan(SHRCMoveBridge,[[motor1, 1, 10, 10], [motor2, 1, 10, 10]], [Keithley2100ViewerBridge])
    # print(gene.array_scan)