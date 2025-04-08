from bluesky import RunEngine
from ophyd import Signal, SignalRO
from bluesky.plans import scan
from bluesky.plans import grid_scan
from bluesky.plans import count
from bluesky.sim import motor1, motor2, motor3, motor4, motor5, motor6


class GenericScan:
    def __init__(self, name_scan):
        self.RE = RunEngine()
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
        class_done = class_name(name = "daichi doesn't know what to do")
        components = list(class_done.component_names)
        self.RE(grid_scan(class_done,
                        motor1, ))
  
        

    def run_viewer(self, class_name):
        class_done = class_name(name = "daichi doesn't know when to stop and listen at times")
        components = list(class_done.component_names)
        
          

 

