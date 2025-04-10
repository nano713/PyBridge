from bluesky import RunEngine
from ophyd import Signal, SignalRO
from bluesky.plans import scan
from bluesky.plans import grid_scan
from bluesky.plans import count
from bluesky.sim import motor1, motor2, motor3, motor4, motor5, motor6


class GenericScan:
    def __init__(self, name_scan, array ):
        self.RE = RunEngine()
        self.has_attribites(name_scan)
        self.array_scan = []
        self.motor = []
        self.array_scan.append(array)

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
        class_done = class_name(name = "test")
        components = list(class_done.component_names)
        grid_scan_args = [class_done]
        for scan in self.array_scan:
            if len(scan) > 1:
                motor = scan[0]
                start,stop,step = scan[1:]
                grid_scan_args.extend([motor, start, stop, step])
        self.RE(grid_scan(*grid_scan_args)) # Extends the grid scan with dynamic motor and scan values
 
         

    def run_viewer(self, class_name):
        class_done = class_name(name = "daichi doesn't know when to stop and listen at times")
        components = list(class_done.component_names)
        grid_scan_args = [class_done]
        for scan in self.array_scan:
            if len(scan) > 1:
                motor = scan[0]
                start,stop,step = scan[1:]
                grid_scan_args.extend([motor, start, stop, step])
        self.RE(scan(*grid_scan_args))
 

