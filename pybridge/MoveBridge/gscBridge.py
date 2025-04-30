from ophyd.signal import Signal, SignalRO
from ophyd.device import Device, Component as Cpt
from pybridge.hardware_bridge.gsc_VISADriver import GSC
from ophyd.status import MoveStatus
from ophyd.pv_positioner import PVPositioner

class GSCMoveBridge(PVPositioner):
    setpoint = Cpt(Signal) #target position
    readback = Cpt(SignalRO) #Read position
    done = Cpt(Signal, value = False) #Instrument is done moving
    actuate = Cpt(Signal) #Request to move
    stop_signal =  Cpt(Signal) #Request to stop

    axis_component = Cpt(Signal, value=1, kind="config")
    speed_ini = Cpt(Signal, value=2000, kind="config")
    speed_fin = Cpt(Signal, value=20000, kind="config")
    accel_t = Cpt(Signal, value=100, kind="config")
    # store_position = Cpt(Signal, value=0.0, kind="hinted")
    loop = Cpt(Signal, value=0, kind="config")
    unit = Cpt(Signal, value="um", kind="config")

    def __init__(
        self,
        prefix="",
        *,
        limits=None,
        name=None,
        read_attrs=None,
        configuration_attrs=None,
        parent=None,
        egu="",
        driver = None,
        **kwargs,
    ):
        super().__init__(
            prefix=prefix,
            read_attrs=read_attrs,
            configuration_attrs=configuration_attrs,
            name=name,
            parent=parent,
            **kwargs,
        )
        #Daichi forced me to stip
        if isinstance(driver, GSC):
            self.gsc = driver
        elif driver is not None:
            self.gsc = GSC(driver)
        else:
            raise ValueError("Driver must be a GSC instance or a valid COM port string.") 
        self.setpoint.put = self.move_relative
        self.readback.get = self.get_position


    def move(self, position: float, wait=True, timeout=None):
        self.setpoint.put(position)
        value = self.gsc.move(self.setpoint.get(), self.axis_component.get())
        print(value)
        status = MoveStatus(self, target = position, timeout = timeout, settle_time = self._settle_time)
        if value == 1: 
            self.done.put(value = True) 
            print("done true")
        else: 
            self.done.put(value = False)
            print("done false")
        status.set_finished()
        return status 

    def get_position(self): 
        return self.gsc.get_position(self.axis_component.get())
    
    def home(self):
        self.gsc.home(self.axis_component.get())
    
    def move_relative(self, position):
        target_position = self.readback.get() + position 
        self.gsc.move_rel(target_position, self.axis_component.get())
    
    def close(self):
        self.gsc.close()
        
class GSCAxis(GSCMoveBridge):
    def __init__(
        self,
        prefix="",
        *,
        limits=None,
        name=None,
        read_attrs=None,
        configuration_attrs=None,
        parent=None,
        egu="",
        axis = 1,
        driver = None,
        **kwargs,
    ):
        super().__init__(
            prefix=prefix,
            read_attrs=read_attrs,
            configuration_attrs=configuration_attrs,
            name=name,
            parent=parent,
            driver=driver,
            **kwargs,
        )
        
        self.axis = axis
        self.gsc = driver
        self.axis_component.put(self.axis)
        self.readback.get = self.get_position
        self.setpoint.put = self.move
    
    def get_position(self):
        return self.gsc.get_position(self.axis)
    
    def move_relative(self, position):
        self.gsc.move_rel(position, self.axis)
    
    def move(self, position: float, wait=True, timeout=None):
        self.gsc.move(position, self.axis)
      
if __name__ == "__main__":
    from pybridge.MoveBridge.gscBridge import GSCAxis, GSCMoveBridge
    gsc = GSC("ASRL4::INSTR")
    from pybridge.hardware_bridge.gsc_VISADriver import GSC

    gsc = GSC("ASRL4::INSTR")

    x = GSCAxis(axis=1, driver=gsc, name="x")
    y = GSCAxis(axis=2, driver=gsc, name="y")
    gsc = GSC("ASRL3::INSTR")
    z = GSCAxis(axis=1, driver=gsc, name="z")