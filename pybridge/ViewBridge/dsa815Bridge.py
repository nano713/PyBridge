from ophyd import Component as Cpt
from ophyd import Device, Signal
from ophyd import SignalRO
from pybridge.hardware_bridge.rigolDSA815_VISADriver import  RigolDSA815VISADriver as DSA815


class DSA815ViewBridge(Device):
    start_frequency = Cpt(Signal, kind="config", metadata={"units": "Hz"})
    stop_frequency = Cpt(Signal, kind = "hinted", metadata={"units": "Hz"})
    center_frequency = Cpt(Signal, kind = "hinted", metadata={"units": "Hz"})
    sweep_time = Cpt(Signal, kind = "hinted")
    amplitude = Cpt(SignalRO, kind="hinted", metadata={"units": "dBm"})
    frequencies = Cpt(SignalRO, kind="hinted", metadata={"units": "Hz"})

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
        
        self.start_frequency.put = self.set_start_frequency 
        self.start_frequency.get = self.get_start_frequency
        self.stop_frequency.put = self.set_stop_frequency
        self.stop_frequency.get = self.get_stop_frequency
        self.center_frequency.put = self.set_center_frequency
        self.center_frequency.get = self.get_center_frequency
        self.sweep_time.put = self.set_sweep_time
        self.sweep_time.get = self.get_sweep_time
        self.frequencies.get = self.get_frequencies
        self.amplitude.get = self.get_trigger_data
    
    def set_start_frequency(self, start_freq):
        self.dsa815.set_start_frequency(start_freq)
    
    def get_start_frequency(self):
        return self.dsa815.get_start_frequency()
    
    def set_stop_frequency(self, stop_freq):
        self.dsa815.set_stop_frequency(stop_freq)
    
    def get_stop_frequency(self):
        return self.dsa815.get_stop_frequency()

    def set_center_frequency(self, center_freq):
        self.dsa815.set_center_frequency(center_freq)
    
    def get_center_frequency(self):
        return self.dsa815.get_center_frequency()
    
    def set_sweep_time(self, sweep_time):
        self.dsa815.set_sweep_time(sweep_time)
    
    def get_sweep_time(self):
        return self.dsa815.get_sweep_time()
    
    def set_frequency_step(self, freq_step):
        self.dsa815.set_frequency_step(freq_step)
    
    def get_frequency_step(self):
        return self.dsa815.get_frequency_step()

    def get_frequencies(self):
        freq = self.dsa815.frequencies_array()

        return freq
            
    def get_trigger_data(self):
        amplitude = self.dsa815.get_trace(number =1)

        return amplitude

if __name__ == "__main__":
    from pybridge.ViewBridge.dsa815Bridge import DSA815ViewBridge
    dsa = DSA815ViewBridge(name="DSA815",driver="USB0::0x1AB1::0x0960::DSA8A154202508::INSTR")
    dsa.start_frequency.put(1e9)
    dsa.stop_frequency.put(2e9)
    dsa.sweep_time.put(0.1)
    dsa.run_amplitude()