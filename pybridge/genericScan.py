from bluesky import RunEngine
from ophyd import Signal
from bluesky.plans import scan


class GenericScan:
    def __init__(self, name_scan):
        self.RE = RunEngine()
        self.has_attribites(name_scan)
    def has_attribites(self, name_scan):
        class_name = name_scan.__class__.__name__

        if "MoveBridge" in class_name:
            self.run_move(name_scan)
        elif "ViewerBridge" in class_name:
            self.run_viewer(name_scan)
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


