from bluesky import RunEngine
from ophyd import Signal, SignalRO
from bluesky.plans import scan
from bluesky.plans import grid_scan
from bluesky.plans import count
from ophyd.sim import motor1, motor2, motor3, det1, det2, det3, det4


class GenericScan:
    def __init__(self, name_scan, array, detectors):
        self.RE = RunEngine()
        self.motor = []
        self.dets = []
        self.create_instance(detectors)
        self.array_scan = array
        # print("print array_scan = ", self.array_scan)
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
            # self.run_move(name_scan)
            print("MoveBridge")
        elif "ViewerBridge" in class_string:
            # self.run_viewer(name_scan)
            print("ViewerBridge")
        else:
            raise ValueError(f"Unknown scan type: {name_scan}")
    
    # def number_of_dets(self, number):
    #     self.detector = []
    #     for i in range(number):
    #         self.detector.append(self.dets[i])
    #     return self.detector
    
    def run_move(self, class_name):
        from bluesky.callbacks.best_effort import BestEffortCallback
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
            # print(grid_scan_args)
                
        print("self.dets,*grid_scan_args =", self.dets,*grid_scan_args)
        self.RE(grid_scan(self.dets,*grid_scan_args)) # Extends the grid scan with dynamic motor and scan values
        # grid_scan([motor1], motor1, 0, 10, 1, motor2, 0, 5, 0.5, motor3, 0, 20, 2)
 
         

    # def run_viewer(self, class_name):
    #     class_done = class_name(name = "daichi doesn't know when to stop and listen at times")
    #     components = list(class_done.component_names)
    #     grid_scan_args = [class_done]
    #     for scan in self.array_scan:
    #         if len(scan) > 1:
    #             motor = scan[0]
    #             start,stop,step = scan[1:]
    #             grid_scan_args.extend([motor, start, stop, step])
    #     self.RE(scan(*grid_scan_args))
 

if __name__ == "__main__":
    from ophyd.sim import motor1, motor2, motor3, det1, det2, det3, det4
    from pybridge.MoveBridge.shrcBridge import SHRCMoveBridge
    from pybridge.ViewBridge.interface_Keithely2100 import Keithley2100ViewerBridge
    from pybridge.genericScan import GenericScan
    # Example usage
    
    class_name = SHRCMoveBridge # or "ViewerBridge"
    shrc = SHRCMoveBridge(name="shrc")
    # array_scan = [
    #     [motor1, 0, 10, 1],
    #     # [motor2, 0, 5, 0.5],
    #     # [motor3, 0, 20, 2]
    # ]

    # scan = GenericScan(class_name, array_scan)
    # gene = GenericScan(SHRCMoveBridge,[[motor1, 1, 10, 10], [motor2, 1, 10, 10]], [Keithley2100ViewerBridge])
    gene = GenericScan(SHRCMoveBridge,[[motor1, 1, 10, 10], [motor2, 1, 10, 10]], [Keithley2100ViewerBridge])
    # print(gene.array_scan)