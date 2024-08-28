""" Orthogonal matrix used to rotate coordindate space"""
import vector3
import euler_angles
import quarternion

class RotationMatrix:
    def __init__(self):
        self.m11 = 0
        self.m12 = 0 
        self.m13 = 0 
        self.m21 = 0 
        self.m22 = 0 
        self.m23 = 0 
        self.m31 = 0 
        self.m32 = 0 
        self.m33 = 0
    def identity(self):
        self.m11 = 1.0; self.m12 = 0.0; self.m13 = 0.0
        self.m21 = 0.0; self.m22 = 1.0; self.m23 = 0.0
        self.m31 = 0.0; self.m32 = 0.0; self.m33 = 1.0

    def setup(self, orientation):
        """setup matrix with specified orientation
        
        Args:
            orientation - euler_angles.EulerAngles
        """
        c_heading, s_heading = quarternion.cos_sin(orientation.heading)
        c_pitch, s_pitch = quarternion.cos_sin(orientation.pitch)
        c_bank, s_bank = quarternion.cos_sin(orientation.bank)
        self.m11 = c_heading*c_bank + s_heading*s_pitch*s_bank
        self.m12 = -c_heading*s_bank + s_heading*s_pitch*c_bank
        self.m13 = s_heading*c_pitch

        self.m21 = s_bank*c_pitch
        self.m22 = c_bank*c_pitch
        self.m23 = -s_pitch

        self.m31 = -s_heading*c_bank + c_heading*s_pitch*s_bank
        self.m32 = s_bank*s_heading + c_heading*s_pitch*c_bank
        self.m33 = c_heading*c_pitch

    def from_inertial_to_object_quarternion(self, q):
        """
        Setup the matrix transformation for a quarternion

        Args:
            q - quarternion.Quarternion
        """
        self.m11 = 1.0 - 2.0*(q.y*q.y + q.z*q.z)
        self.m12 = 2.0 * (q.x*q.y + q.w*q.z)
        self.m13 = 2.0 * (q.x*q.z - q.w*q.y) 
        self.m21 = 2.0 * (q.x*q.y - q.w*q.z)
        self.m22 = 1.0 - 2.0 * (q.x*q.x + q.z*q.z)
        self.m23 = 2.0 * (q.y*q.z + q.w*q.x)
        self.m31 = 2.0 * (q.x*q.z + q.w*q.y)
        self.m32 = 2.0 * (q.y*q.z - q.w*q.x)
        self.m33 = 1.0 - 2.0 * (q.x*q.x + q.y*q.y)
    
    def from_object_to_inertial_quarternion(self, q):
        """
        Setup the matrix transformation for a quarternion

          Args:
            q - quarternion.Quarternion
        """
        self.m11 = 1.0 - 2.0 * (q.y*q.y + q.z*q.z)
        self.m12 = 2.0 * (q.x*q.y - q.w*q.z)
        self.m13 = 2.0 * (q.x*q.z + q.w*q.y)
        self.m21 = 2.0 * (q.x*q.y + q.w*q.z)
        self.m22 = 1.0 - 2.0 * (q.x*q.x + q.z*q.z)
        self.m23 = 2.0 * (q.y*q.z - q.w*q.x)
        self.m31 = 2.0 * (q.x*q.z - q.w*q.y)
        self.m32 = 2.0 * (q.y*q.z + q.w*q.x)
        self.m33 = 1.0 - 2.0 * (q.x*q.x + q.y*q.y)
    # perform rotations 
    def inertial_to_object(self,v: vector3.Vector3):
        return vector3.Vector3(
            self.m11*v.x + self.m21*v.y + self.m31*v.z, 
            self.m12*v.x + self.m22*v.y + self.m32*v.z,
            self.m13*v.x + self.m23*v.y + self.m33*v.z
        )
    def object_to_inertial(self, v: vector3.Vector3):
        return vector3.Vector3(
            self.m11*v.x + self.m12*v.y + self.m13*v.z,
            self.m21*v.x + self.m22*v.y + self.m23*v.z,
            self.m31*v.x + self.m32*v.y + self.m33*v.z
        )
    
    