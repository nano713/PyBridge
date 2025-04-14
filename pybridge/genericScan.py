from bluesky import RunEngine
from ophyd import Signal, SignalRO
from bluesky.plans import scan
from bluesky.plans import grid_scan
from bluesky.plans import count
from ophyd.sim import motor1, motor2, motor3, det1, det2, det3, det4


class GenericScan:
    def __init__(self, name_scan, array):
        self.RE = RunEngine()
      
        
        self.array_scan = []
        self.motor = []
        self.dets = [det1,det2,det3,det4]
        self.array_scan.append(array)
        print(self.array_scan)
        self.has_attribites(name_scan)

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
            self.run_move(name_scan)
            print("MoveBridge")
        elif "ViewerBridge" in class_string:
            self.run_viewer(name_scan)
            print("ViewerBridge")
        else:
            raise ValueError(f"Unknown scan type: {name_scan}")
    
    def run_move(self, class_name):
        from bluesky.callbacks.best_effort import BestEffortCallback
        bec = BestEffortCallback()

        # Send all metadata/data captured to the BestEffortCallback.
        self.RE.subscribe(bec)  
                
        class_done = class_name(name = "test")
        # components = list(class_done.component_names)
        grid_scan_args = []
        dets = []
        print("Error passed")
        for i, scan in enumerate(self.array_scan): 
            motor = scan[0]
            dets.append(self.dets[i])
            start,stop,step = scan[1:]
            grid_scan_args.append(motor)
            grid_scan_args.append(start)
            grid_scan_args.append(stop)
            grid_scan_args.append(step)
            print(grid_scan_args)
                
        print("dets = ", dets)
        print("grid_scan_args =", grid_scan_args)
        self.RE(grid_scan(dets,*grid_scan_args)) # Extends the grid scan with dynamic motor and scan values
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
    from ophyd.sim import motor1, motor2, motor3
    from pybridge.MoveBridge.shrcBridge import SHRCMoveBridge
    from pybridge.genericScan import GenericScan
    # Example usage
    
    class_name = SHRCMoveBridge # or "ViewerBridge"
    # array_scan = [
    #     [motor1, 0, 10, 1],
    #     # [motor2, 0, 5, 0.5],
    #     # [motor3, 0, 20, 2]
    # ]

    # scan = GenericScan(class_name, array_scan)
    gene = GenericScan(SHRCMoveBridge, [motor1, 1,10,10])
    print(gene.array_scan)