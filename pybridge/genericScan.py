from bluesky import RunEngine
from ophyd import Signal
from bluesky.plans import scan


class GenericScan:
    def __init__(self, name_scan):
        self.RE = RunEngine()
        self.has_attribites(name_scan)
    def has_attribites(self, name_scan):
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
        components = []
        for attr in dir(class_name):
            if hasattr(class_name, attr) and isinstance(getattr(class_name, attr), Signal):
                components.append(attr)
        return components
        

    def run_viewer(self, class_name):
        pass
 

