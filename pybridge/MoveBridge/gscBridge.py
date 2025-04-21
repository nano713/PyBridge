from ophyd.signal import Signal, SignalRO

class GSCMoveBridge:
    def __init__(self, com):
        self.gsc = com
