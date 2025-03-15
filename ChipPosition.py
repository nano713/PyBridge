# Takes coordinates from a Si chip from an optical microscope with the purpose to find the center of the chip
# and the distance between the holes in the chip 


import numpy as np
import os 
import pandas as pd 
from ophyd import Component as Cpt
from ophyd import SoftPositioner, PVPositioner
from hardware_bridge.shot304_VISADriver import SHOT304VISADriver
from ophyd.pseudopos import (PseudoPositioner, PseudoSingle)


class SiChipPosition():
    # pos_x = Cpt(PVPositioner, limits=(-10, 10))
    # pos_y = Cpt(PVPositioner, limits=(-10, 10))
    # pos_z = Cpt(PseudoSingle, limits=(-10, 10))

    def __init__(self, *args, **kwargs): 
        self.position = SHOT304VISADriver("ASRL3::INSTR")
        self.position.open_connection()
        # super().__init__(*args, **kwargs)
    
    def get_chip_coordinates(self):
        """Get the coordinates of the chip from the microscope."""
        x = self.position.get_position(1)
        y = self.position.get_position(2)
        z = self.position.get_position(3)
        return x, y, z
    
    def get_relative_coordinates(self, refence_point): 

        x, y, z = self.get_chip_coordinates()
        print("x type", type(x))
        print("refence_point[0] type", type(refence_point[0]))
        x = x - refence_point[0]
        y = y - refence_point[1]
        z = z - refence_point[2]
        return x, y, z
    
    def calculate_transformation_matrix(self, reference_point, target_point):
        """Calculate the transformation matrix."""
        reference_point = np.array(reference_point)
        target_point = np.array(target_point)

        reference_center = np.mean(reference_point, axis=0)
        target_center = np.mean(target_point, axis=0)

        reference_point = reference_point = reference_center
        target_point = target_point - target_center

        covariance_matrix = np.dot(reference_point.T, target_point)
        U, S, V = np.linalg.svd(covariance_matrix)

        rotation_matrix = np.dot(V.T, U.T)
        translation_matrix = target_center.T - np.dot(rotation_matrix, reference_center.T)
        transformation_matrix = np.zeros((4, 4))
        transformation_matrix[:3, :3] = rotation_matrix # 3x3 rotation matrix
        transformation_matrix[:3, 3] = translation_matrix # 3x1 translation matrix
        return transformation_matrix
    
    def apply_transformation_matrix(self, transformation_matrix, x, y, z):
        coordinates = np.array([x, y, z])
        transformation_matrix = np.dot(transformation_matrix, coordinates)
        return transformation_matrix
    


    def compute_center(self, x, y, z): 
        """ Computes the center of the chip"""
        center_x = np.mean(x)
        center_y = np.mean(y)
        center_z = np.mean(z)
        return center_x, center_y, center_z

if __name__ == "__main__":
    shrc = SiChipPosition(name="shrc")
    x, y, z = shrc.get_chip_coordinates()
    print("get_chip_coordinates", x, y, z)

    refernce_point = np.array([0, 0, 0])
    x, y, z = shrc.get_relative_coordinates(refernce_point)
    print("get_relative_coordinates", x, y, z)

    reference_point = np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0], [1, 1, 0]])
    target_point = np.array([[0, 0, 0], [0, 1, 0], [1, 0, 0], [1, 1, 0]])   

    transformation_matrix = shrc.calculate_transformation_matrix(reference_point, target_point)
    print("transformation_matrix", transformation_matrix)

    x, y, z = shrc.apply_transformation_matrix(transformation_matrix, x, y, z)
    print("apply_transformation_matrix", x, y, z)

    center_x, center_y, center_z = shrc.compute_center(x, y, z)
    print("compute_center", center_x, center_y, center_z) 
    
    shrc.close_connection()

