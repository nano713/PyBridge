# Takes coordinates from a Si chip from an optical microscope with the purpose to find the center of the chip
# and the distance between the holes in the chip 


import numpy as np


# from ophyd.sim import motor


class SiChipPosition():
    
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

        self.center_x, self.center_y, self.center_z = self.compute_center(x0,y0,z0,x1,y1,z1,x2,y2,z2) # P
        print(f"center_x: {self.center_x}, center_y: {self.center_y}, center_z: {self.center_z}")
        rel_point0 = np.array([x0- self.center_x, y0 - self.center_y, z0 - self.center_z])
        rel_point1 = np.array([x1- self.center_x, y1 - self.center_y, z1 - self.center_z])
        rel_point2 = np.array([x2- self.center_x, y2 - self.center_y, z2 - self.center_z])

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


        theta_phi = np.arctan2(rel_point0[2], rel_point0[0])
        rotation_matrix_phi = np.array([
            [np.cos(theta_phi), 0, np.sin(theta_phi)],
            [0, 1, 0],
            [-np.sin(theta_phi), 0, np.cos(theta_phi)]
        ])

        rel_point0 = np.dot(rotation_matrix_phi, rel_point0)
        rel_point1 = np.dot(rotation_matrix_phi, rel_point1)
        rel_point2 = np.dot(rotation_matrix_phi, rel_point2)

        print(f"rel_point0: {rel_point0}, rel_point1: {rel_point1}, rel_point2: {rel_point2}, thetha_horiz: {thetha_horiz}, theta_vertical: {theta_vertical}, theta_phi: {theta_phi}")
        return rel_point0, rel_point1, rel_point2, thetha_horiz, theta_vertical, theta_phi
        
    def calculate_transformation_matrix(self, x0,y0,z0,x1,y1,z1,x2,y2,z2):
        """Calculate the transformation matrix."""
        rel_point0, rel_point1, rel_point2, thetha_horiz, theta_vertical, theta_phi = self.get_relative_coordinates(x0,y0,z0,x1,y1,z1,x2,y2,z2)
        
        relative_point = np.array([rel_point0, rel_point1, rel_point2])
        target_point = np.array([[x0, y0, z0], [x1, y1, z1], [x2, y2, z2]])

        T = np.dot(np.linalg.pinv(relative_point), target_point)
        print(f"T.shape: {T.shape}")
        T_convert = np.identity(4)
        T_convert[:3, :3] = T
        return T# T_convert
    
    def apply_transformation_matrix(self, transformation_matrix, x, y, z):
        # coordinates = np.array([x, y, z, 1])
        coordinates = np.array([x, y, z])
        center = np.array([self.center_x, self.center_y, self.center_z])
        coordinates = coordinates - center
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
    # x0,y0,z0 = -1000,1100,100 # left top
    # x1,y1,z1 = 1000,900,100 # right top
    # x2,y2,z2 = -1000,-1000,90 # left bottom
    # x3, y3, z3 = -500, 525, 100 # compute the relative coordinate of this point
    # matrix = shot.calculate_transformation_matrix(x0,y0,z0,x1,y1,z1,x2,y2,z2)
    # print(f"matrix {matrix}")
    # tranform_coordinates = shot.apply_transformation_matrix(matrix, x3, y3, z3)
    # print(f"tranform_coordinates {tranform_coordinates}")
    


    