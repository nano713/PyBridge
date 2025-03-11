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
        


    def compute_center(self, x, y, z): 
        """ Computes the center of the chip"""
        center_x = np.mean(x)
        center_y = np.mean(y)
        center_z = np.mean(z)
        return center_x, center_y, center_z
