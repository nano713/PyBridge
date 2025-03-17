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
    
# P' = 
# T = P'-1 .P
# P' = T . P
    def get_relative_coordinates(self, x0,y0,z0,x1,y1,z1,x2,y2,z2): 

        center_x, center_y, center_z = self.compute_center(x0,y0,z0,x1,y1,z1,x2,y2,z2) # P
        rel_point0 = np.array([x0- center_x, y0 - center_y, z0 - center_z])
        rel_point1 = np.array([x1- center_x, y1 - center_y, z1 - center_z])
        rel_point2 = np.array([x2- center_x, y2 - center_y, z2 - center_z])

        thetha_horiz = np.arctan2(rel_point1[1] - rel_point0[1], rel_point1[0] - rel_point0[0])
        rotation_matrix_horiz = np.array([
            [np.cos(thetha_horiz), -np.sin(thetha_horiz), 0],
            [np.sin(thetha_horiz), np.cos(thetha_horiz), 0],
            [0, 0, 1]
        ])
        rel_point0 = np.dot(rotation_matrix_horiz, rel_point0)
        rel_point1 = np.dot(rotation_matrix_horiz, rel_point1)
        rel_point2 = np.dot(rotation_matrix_horiz, rel_point2)

        theta_vertical = np.arctan2(rel_point0[2], rel_point0[1])
        rotation_matrix_vertical = np.array([
            [1, 0, 0],
            [0, np.cos(theta_vertical), -np.sin(theta_vertical)],
            [0, np.sin(theta_vertical), np.cos(theta_vertical)]
        ])
        rel_point0 = np.dot(rotation_matrix_vertical, rel_point0)
        rel_point1 = np.dot(rotation_matrix_vertical, rel_point1)
        rel_point2 = np.dot(rotation_matrix_vertical, rel_point2)

        print(f"rel_point0: {rel_point0}, rel_point1: {rel_point1}, rel_point2: {rel_point2}, thetha_horiz: {thetha_horiz}, theta_vertical: {theta_vertical}")
        return rel_point0, rel_point1, rel_point2, thetha_horiz, theta_vertical
        
    def calculate_transformation_matrix(self, x0,y0,z0,x1,y1,z1,x2,y2,z2):
        """Calculate the transformation matrix."""
        rel_point0, rel_point1, rel_point2, thetha_horiz, theta_vertical = self.get_relative_coordinates(x0,y0,z0,x1,y1,z1,x2,y2,z2)
        
        relative_point = np.array([rel_point0, rel_point1, rel_point2])
        target_point = np.array([[x0, y0, z0], [x1, y1, z1], [x2, y2, z2]])

        T = np.dot(np.linalg.pinv(relative_point), target_point)
        T_convert = np.identity(4)
        T_convert[:3, :3] = T
        return T_convert
    def apply_transformation_matrix(self, transformation_matrix, x, y, z):
        coordinates = np.array([x, y, z, 1])
        transformation_matrix = np.dot(transformation_matrix, coordinates)
        return transformation_matrix[:3]

    def compute_center(self, x0, y0, z0, x1, y1, z1, x2, y2, z2): 
        """ Computes the center of the chip"""
        mid_top_x = (x0 + x1) / 2
        mid_top_y = (y0 + y1) / 2
        mid_top_z = (z0 + z1) / 2

        mid_left_x = (x0 + x2) / 2
        mid_left_y = (y0 + y2) / 2
        mid_left_z = (z0 + z2) / 2

        center_x = (mid_top_x + mid_left_x) / 2
        center_y = (mid_top_y + mid_left_y) / 2
        center_z = (mid_top_z + mid_left_z) / 2

        return center_x, center_y, center_z
        

if __name__ == "__main__":
    shot = SiChipPosition()
    x0,y0,z0 = -1000,1000,100 # left top
    x1,y1,z1 = 1000,1000,100 # right top
    x2,y2,z2 = -1000,-1000,100 # left bottom
    x3, y3, z3 = 100, 100, 100 # compute the relative coordinate of this point

    rel_point0, rel_point1, rel_point2, thetha_horiz, theta_vertical = shot.get_relative_coordinates(x0,y0,z0,x1,y1,z1,x2,y2,z2)
    # center_x, center_y, center_z = shot.compute_center(x,y,z)
    print(f"x: {rel_point0}, y: {rel_point1}, z: {rel_point2}, thetha_horiz: {thetha_horiz}, theta_vertical: {theta_vertical}")
    matrix = shot.calculate_transformation_matrix(x0,y0,z0,x1,y1,z1,x2,y2,z2)
    print(f"matrix {matrix}")
    tranform_coordinates = shot.apply_transformation_matrix(matrix, rel_point0[0], rel_point1[0], rel_point2[0])
    print(f"tranform_coordinates {tranform_coordinates}")
    


    