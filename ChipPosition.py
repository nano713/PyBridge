# Takes coordinates from a Si chip from an optical microscope with the purpose to find the center of the chip
# and the distance between the holes in the chip 


import numpy as np
import os 
import pandas as pd 
from ophyd import Component as Cpt
from ophyd import SoftPositioner, PVPositioner
from hardware_bridge.shot304_VISADriver import SHOT304VISADriver
from ophyd.pseudopos import (PseudoPositioner, PseudoSingle)
# from ophyd.sim import motor


class SiChipPosition():
    # pos_x = Cpt(PVPositioner, limits=(-10, 10))
    # pos_y = Cpt(PVPositioner, limits=(-10, 10))
    # pos_z = Cpt(PseudoSingle, limits=(-10, 10))

    # def __init__(self, *args, **kwargs): 
        # self.position = SHOT304VISADriver("ASRL3::INSTR")
        # self.position.open_connection()
        # super().__init__(*args, **kwargs)
    
    def get_chip_coordinates(self):
        """Get the coordinates of the chip from the microscope."""
        x = self.position.get_position(1)
        y = self.position.get_position(2)
        z = self.position.get_position(3)
        return np.array([x, y, z])
    

    def get_relative_coordinates(self, x0,y0,z0,x1,y1,z1,x2,y2,z2): 

        reference_points = np.array([x0,y0,z0])
        target_points = np.array([x1,y1,z1], [x2,y2,z2], )
        relative_points = target_points - reference_points  
        x = relative_points[:,0]
        y = relative_points[:,1]
        z = relative_points[:,2]

        tilt_x = np.arctan2(y[1] - y[0], z[1] - z[0])
        tilt_y = np.arctan2(x[1] - x[0], z[1] - z[0])
        tilt_z = np.arctan2(y[1] - y[0], x[1] - x[0])

        return x, y, z, tilt_x, tilt_y, tilt_z
        
    def calculate_transformation_matrix(self, x0,y0,z0,x1,y1,z1,x2,y2,z2):
        """Calculate the transformation matrix."""
        x,y,z, tilt_x, tilt_y, tilt_z = self.get_relative_coordinates(x0,y0,z0,x1,y1,z1,x2,y2,z2)

        reference_point = np.array([x[0], y[0], z[0]])
        target_point = np.array([x[1], y[1], z[1]], [x[2], y[2], z[2]])

        reference_center = np.mean(reference_point, axis=0)
        target_center = np.mean(target_point, axis=0)

        reference_point = reference_point - reference_center
        target_point = target_point - target_center

        covariance_matrix = np.dot(reference_point.T, target_point)
        U, S, V = np.linalg.svd(covariance_matrix)

        rotation_matrix = np.dot(V.T, U.T)
        if np.linalg.det(rotation_matrix) < 0:
            V[-1, :] *= -1
            rotation_matrix = np.dot(V.T, U.T)

        translation_matrix = target_center.T - np.dot(rotation_matrix, reference_center.T)
        transformation_matrix = np.identity(4)
        transformation_matrix[:3, :3] = rotation_matrix # 3x3 rotation matrix
        transformation_matrix[:3, 3] = translation_matrix # 3x1 translation matrix

        tilt_matrix_x = np.array([1,0,0,0], [0, np.cos(tilt_x), -np.sin(tilt_x), 0], [0, np.sin(tilt_x), np.cos(tilt_x), 0], [0,0,0,1])
        tilt_matrix_y = np.array([np.cos(tilt_y), 0, np.sin(tilt_y), 0], [0,1,0,0], [-np.sin(tilt_y), 0, np.cos(tilt_y), 0], [0,0,0,1])
        tilt_matrix_z = np.array([np.cos(tilt_z), -np.sin(tilt_z), 0, 0], [np.sin(tilt_z), np.cos(tilt_z), 0, 0], [0,0,1,0], [0,0,0,1])

        transformation_matrix = np.dot(transformation_matrix, tilt_matrix_x)
        transformation_matrix = np.dot(transformation_matrix, tilt_matrix_y)
        transformation_matrix = np.dot(transformation_matrix, tilt_matrix_z)

        transformation_matrix = self.apply_transformation_matrix(transformation_matrix, x0, y0, z0)

        return transformation_matrix
    
    def apply_transformation_matrix(self, transformation_matrix, x, y, z):
        coordinates = np.array([x, y, z, 1])
        transformation_matrix = np.dot(transformation_matrix, coordinates)
        return transformation_matrix[:3]

    def compute_center(self, x, y, z): 
        """ Computes the center of the chip"""
        center_x = np.mean(x)
        center_y = np.mean(y)
        center_z = np.mean(z)
        return center_x, center_y, center_z

if __name__ == "__main__":
    shot = SiChipPosition()
    x0,y0,z0 = 1,1,1
    x1,y1,z1 = 2,2,2
    x2,y2,z2 = 3,3,3
    x, y, z = shot.get_relative_coordinates(x0,y0,z0,x1,y1,z1,x2,y2,z2)
    matrix = shot.calculate_transformation_matrix(x0,y0,z0,x1,y1,z1,x2,y2,z2)
    tranform_coordinates = shot.apply_transformation_matrix(matrix, x[0], y[0], z[0])
    print(tranform_coordinates)
    


    