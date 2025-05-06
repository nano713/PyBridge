from ophyd import Component as Cpt
from ophyd import Device, Signal
from ophyd import SignalRO
from pybridge.hardware_bridge.rigolDSA815_VISADriver import RigolDSA815 as DSA815


class DSA815ViewBridge(Device):
    start_frequency = Cpt(Signal, kind="config", metadata={"units": "Hz"})
    stop_frequency = Cpt(Signal, kind = "hinted", metadata={"units": "Hz"})
    center_frequency = Cpt(Signal, kind = "hinted", metadata={"units": "Hz"})
    sweep_time = Cpt(Signal, kind = "hinted")
    amplitude = Cpt(SignalRO, kind="hinted", metadata={"units": "dBm"})
    frequencies = Cpt(SignalRO)

    def __init__(
            self,
            prefix="",
            *,
            name,
            parent=None, kind=None,
            driver = None,
            **kwargs,
    ):
        super().__init__(name=name, parent=parent, kind=kind, **kwargs)
    
        self.dsa815 = DSA815(driver)
        self.start_frequency.set = self.set_start_frequency 
        self.start_frequency.get = self.get_start_frequency
        self.stop_frequency.set = self.set_stop_frequency
        self.stop_frequency.get = self.get_stop_frequency
        self.center_frequency.set = self.set_center_frequency
        self.center_frequency.get = self.get_center_frequency
        self.sweep_time.set = self.set_sweep_time
        self.sweep_time.get = self.get_sweep_time
        self.amplitude.get = self.get
    

    def set_start_frequency(self, start_freq):
        """"Sets the Start Frequency of the RigolDSA815

        Parmas:
            start_freq (float): value to set the frequency
            """
        self.dsa815.start_frequency = start_freq 
    
    def get_start_frequency(self):
        return self.dsa815.start_frequency

    def set_center_frequency(self, center_freq):
        self.dsa815.center_frequency = center_freq
    
    def get_center_frequency(self):
        return self.dsa815.center_frequency

    def set_stop_frequency(self, stop_freq):
        self.dsa815.stop_frequency = stop_freq
    
    def get_stop_frequency(self):
        return self.dsa815.stop_frequency

    def set_sweep_time(self, sweep_time):
        self.dsa815.sweep_time = sweep_time
    
    def get_sweep_time(self):
        return self.dsa815.sweep_time
    
    def set_frequency_step(self, step_freq):
        self.dsa815.frequency_step = step_freq
    
    def get_frequency_step(self):
        return self.dsa815.frequency_step
    
    def trigger_aplitude(self):
        self.frequencies = self.dsa815.trace_df()
        self.amplitude = self.dsa815.trace()
    
    def get_amplitude_continuous(self):
        if not hasattr(self, "amplitude"):
           raise ValueError("No amplitude data available. Please trigger the device first.")

        for amplitude in self.amplitude:
            yield from amplitude
    
    def run_amplitude(self):
        self.trigger_aplitude()
        for amplitude in self.get_amplitude_continuous():
            print(amplitude)

if __name__ == "__main__":
    from pybridge.ViewBridge.dsa815Bridge import DSA815ViewBridge
    dsa = DSA815ViewBridge(name="DSA815",driver="USB0::0x1AB1::0x0960::DSA8A154202508::INSTR")
    dsa.start_frequency.put(1e9)
    dsa.stop_frequency.put(2e9)
    dsa.sweep_time.put(0.1)
    dsa.run_amplitude()