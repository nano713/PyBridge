# Takes coordinates from a Si chip from an optical microscope with the purpose to find the center of the chip
# and the distance between the holes in the chip 


import numpy as np
import os 
import pandas as pd 
from ophyd import Component as Cpt
from ophyd import SoftPositioner, PVPositioner
from hardware_bridge.shot304_VISADriver import SHOT304VISADriver
from ophyd.pseudopos import (PseudoPositioner, PseudoSingle)


class SiChipPosition(PseudoPositioner):
    pos_x = Cpt(PVPositioner, limits=(-10, 10))
    pos_y = Cpt(PVPositioner, limits=(-10, 10))
    pos_z = Cpt(PseudoSingle, limits=(-10, 10))

    def __init__(self, *args, **kwargs):
        self.position = SHOT304VISADriver("ASRL3::INSTR")
        self.position.open_connection()
        super().__init__(*args, **kwargs)
    
    def get_chip_coordinates(self):
        """Get the coordinates of the chip from the microscope."""
        x = self.position.get_position(1)
        y = self.position.get_position(2)
        z = self.position.get_position(3)
        return x, y, z


    def compute_center(self, x, y, z): 
        """ Computes the center of the chip"""
        center_x = np.mean(x)
        center_y = np.mean(y)
        center_z = np.mean(z)
        return center_x, center_y, center_z
