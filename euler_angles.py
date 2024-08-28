"""Class used to store orientation in euler(oiler) angles using heading, pitch, and bank"""

import math
import quarternion 
import rotation_matrix
import matrix_4x3

class EulerAngles:
    def __init__(self, h = 0.0, p = 0.0, b = 0.0) -> None:
        self.heading = h
        self.pitch = p
        self.bank = b
    def identity(self):
        self.bank = self.pitch = self.heading = 0.0
    def canonize(self):
        self.pitch = wrap(self.pitch)
        if self.pitch < -math.pi/2: 
            self.pitch = -math.pi - math.pi
            self.heading += math.pi
            self.bank += math.pi
        elif self.pitch > math.pi/2:
            self.pitch = math.pi - self.pitch 
            self.heading += math.pi
            self.bank += math.pi

        if abs(self.pitch) > math.pi/2 - 1e-2: 
            # gimbel lock condition 
            self.heading += self.bank # heading controls by bank 
            self.bank = 0
            self.heading = wrap(self.heading)
        else: 
            self.bank = wrap(self.bank)
            self.heading = wrap(self.heading)


    def from_object_to_inertial_quarternion(self, q):
        """Using object --> inertial rotation quarternion , setup angles 
        
        Args:
            q - quaternion
        
        """
        sp = -2.0 * (q.y * q.z - q.w * q.x)
        if abs(sp) >= 1 - 1e-3:
            # gimbal lock condition
            self.pitch = (math.pi/2) * sp
            self.heading = math.atan2(-q.x*q.z + q.w*q.y, 0.5-q.y*q.y-q.z*q.z)
            self.bank = 0.0
        else:
            self.pitch = math.asin(sp)
            self.heading = math.atan2(q.x*q.z + q.w*q.y, 0.5 - q.x*q.x - q.y*q.y)
            self.bank = math.atan2(q.x*q.y + q.w*q.z, 0.5 - q.x*q.x - q.z*q.z)

    def from_inertial_to_object_quarternion(self, q ):
        """Using intertial --> object rotation quarternion, setup angles 
        
        
        Args:
            q - quaternion
        """
        sp = -2.0 * (q.y * q.z + q.w * q.x)
        if abs(sp) > 1-1e-3:
            # gimbal lock condition 
            self.pitch = (math.pi/2) * sp
            self.heading = math.atan2(-q.x*q.z - q.w*q.y, 0.5 - q.y*q.y - q.z*q.z)
            self.bank = 0.0
        else: 
            self.pitch = math.asin(sp)
            self.heading = math.atan2(q.x*q.z - q.w*q.y, 0.5 - q.x*q.x - q.y*q.y)
            self.bank = math.atan2(q.x*q.y - q.w*q.z, 0.5 - q.x*q.x - q.z*q.z)

    def from_object_to_world_matrix_quaternion(self, m: matrix_4x3.Matrix4x3):
        """Using object --> world transformation matrix, setup angles 
        
        
        Args:
            m - matrix4x3 
        """

        sp = -m.m32
        if abs(sp) > 1 - 1e-3:
            # gimbal lock condition
            self.pitch = (math.pi/2) * sp
            self.heading = math.atan2(-m.m23, m.m11)
            self.bank = 0.0
        else: 
            self.heading = math.atan2(m.m31, m.m33)
            self.pitch = math.asin(sp)
            self.bank = math.atan2(m.m12, m.m22)

    def from_world_to_object_matrix_quaternion(self, m: matrix_4x3.Matrix4x3):
        """Using world --> object transformation matrix, setup euler angles 
        
        
        Args:
            m - matrix4x3 
        """
        sp = -m.m23 
        if abs(sp) > 1 - 1e-3:
            # gimbal lock condition 
            self.pitch = (math.pi/2) * sp 
            self.heading = math.atan2(-m.m31, m.m11)
            self.bank = 0 
        else: 
            self.heading = math.atan2(m.m13, m.m33)
            self.pitch = math.asin(sp)
            self.bank = math.atan2(m.m21, m.m22)


    def from_rotation_matrix(self, m: rotation_matrix.RotationMatrix):
        """Using rotation matrix, setup euler angles
        
        
        Args:
            m - RotationMatrix
        """ 
        sp = -m.m23
        if abs(sp) > 1 - 1e-3:
            self.pitch = (math.pi/2) * sp 
            self.heading = math.atan2(-m.m31, m.m11)
            self.bank = 0.0
        else: 
            self.heading = math.atan2(m.m13, m.m33)
            self.pitch = math.asin(sp)
            self.bank = math.atan2(m.m21, m.m22)
        

    
     
# non member functions
def wrap(theta):
    """wraps angle to range [-pi, pi]"""
    theta += math.pi
    theta -= math.floor(theta/(2*math.pi))
    theta -= math.pi
    return theta 

    