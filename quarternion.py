import vector3 
import euler_angles
import math 
import quarternion

class Quarternion():
    def __init__(self) -> None:
        self.w = 1 
        self.x = 0 
        self.y = 0 
        self.z = 0 
    def __repr__(self) -> None:
        return f'Quarternion( w = {self.w}, x = { self.x }, y = { self.y }, z = { self.z } )'
    def identity(self)-> None:
        self.w = 1.0
        self.x = self.y = self.z = 0.0
    def set_to_rotate_about_x(self, theta: float):
        theta_over_2 = theta * 0.5
        self.w = math.cos(theta_over_2)
        self.x = math.sin(theta_over_2)
        self.z = 0.0
        self.y = 0.0
    def set_to_rotate_about_y(self, theta: float):
        theta_over_2 = theta * 0.5
        self.w = math.cos(theta_over_2)
        self.x = 0.0
        self.z = 0.0
        self.y = math.sin(theta_over_2) 
    def set_to_rotate_about_z(self, theta: float):
        theta_over_2 = theta * 0.5
        self.w = math.cos(theta_over_2)
        self.x = 0.0
        self.y = 0.0
        self.z = math.sin(theta_over_2)
    def set_to_rotate_about_axis(self, axis: vector3.Vector3, theta: float):
        # axis must be normalized 
        assert((vector3.vector_mag(axis) - 1.0) < 0.01)
        theta_over_2 = theta * 0.5
        sin_theta_over_2 = math.sin(theta_over_2)
        self.w = math.cos(theta_over_2)
        self.x = axis.x * sin_theta_over_2
        self.y = axis.y * sin_theta_over_2
        self.z = axis.z * sin_theta_over_2
    def set_to_rotate_object_to_inertial(self, orientation: euler_angles.EulerAngles): 
        c_pitch, s_pitch = cos_sin(orientation.pitch*0.5)
        c_heading, s_heading = cos_sin(orientation.heading*0.5)
        c_bank, s_bank = cos_sin(orientation.bank*0.5)
        self.w = c_heading*c_pitch*c_bank + s_heading*s_pitch*s_bank
        self.x = c_heading*s_heading*c_bank + s_heading*c_pitch*s_bank
        self.y = -c_heading*s_pitch*s_bank + s_heading*c_pitch*c_bank
        self.z = -s_heading*s_pitch*c_bank + c_heading*c_pitch*s_bank
    def set_to_rotate_inertial_to_object(self, orientation: euler_angles.EulerAngles): 
        c_pitch, s_pitch = cos_sin(orientation.pitch*0.5)
        c_heading, s_heading = cos_sin(orientation.heading*0.5)
        c_bank, s_bank = cos_sin(orientation.bank*0.5)  
        self.w = c_heading*c_pitch*c_bank + s_heading*s_pitch*s_bank
        self.x = -c_heading*s_pitch*c_bank - s_heading*c_pitch*s_bank
        self.y = c_heading*s_pitch*s_bank - s_heading*c_bank*c_pitch
        self.z = s_heading*s_pitch*c_bank - c_heading*c_pitch*s_bank
    def __mul__(self, q):
        """ 
        cross product
        
        Args:
            q - quarternion
        """
        q_out = Quarternion()
        q_out.w = self.w*q.w - self.x*q.x - self.y*q.y - self.z*q.z
        q_out.x = self.w*q.x + self.x*q.w + self.z*q.y - self.y*q.z
        q_out.y = self.w*q.y + self.y*q.w + self.x*q.z - self.z*q.x
        q_out.z = self.w*q.z + self.z*q.w + self.y*q.x - self.x*q.y
        return q_out
    def __rmul__(self, q):
        return self.__mul__(q)
    def normalize(self):
        mag = math.sqrt(self.w*self.w + self.x*self.x + self.y*self.y + self.z*self.z)
        if mag > 0.0 :
            one_over_mag = 1 / mag 
            self.w *= one_over_mag
            self.x *= one_over_mag
            self.y *= one_over_mag
            self.z *= one_over_mag
        else: 
            self.identity()
    def get_rotation_angle(self):
        """compute rotation angle"""
        theta_over_2 = math.acos(self.w)
        return theta_over_2 * 2.0
    def get_rotation_axis(self):
        """compute 'n' vector"""
        sin_theta_over_2_sq = 1 - self.w*self.w
        if sin_theta_over_2_sq <= 0:
            # identity quarternion, return any valid vector
            return vector3.Vector3(1.0, 0.0, 0.0)
        one_over_sin_theta_over_2 = 1 / math.sqrt(sin_theta_over_2_sq)
        return vector3.Vector3(self.x/one_over_sin_theta_over_2, self.y/one_over_sin_theta_over_2, self.z/one_over_sin_theta_over_2)
    
# non member variables 
def cos_sin(theta: float) -> tuple:
    """Compute sin and cos angle for quaternion."""
    return math.cos(theta), math.sin(theta)
def dot_product(a: Quarternion, b: Quarternion):
    return a.w*b.w + a.x*b.x + a.y*b.y + a.z*b.z
def slerp (q0: Quarternion, q1: Quarternion, t: float) -> Quarternion:
    """interpolates 'start' and 'end' orientations of two unit quarternions"""
    if t <= 0.0 :
        return q0 
    if t >= 1.0:
        return q1 
    cos_omega = dot_product(q0, q1)
    q1w = q1.w
    q1x = q1.x
    q1y = q1.y
    q1z = q1.z
    if cos_omega < 0.0:
        q1w = -q1w
        q1x = -q1x
        q1y = -q1y
        q1z = -q1z
        cos_omega = -cos_omega
    if cos_omega >= 1.1:
        # two quarternions must be unit quarternions 
        raise(RuntimeError)
    if cos_omega > 0.999:
        # dot product is approximaterly one 
        k0 = 1.0-t
        k1 = t
    else:
        sin_omega = math.sqrt(1 - cos_omega*cos_omega)
        omega = math.atan2(sin_omega, cos_omega)
        one_over_sin_omega = 1 / sin_omega
        k0 = math.sin((1.0 - t) * omega) * one_over_sin_omega
        k1 = math.sin(t*omega) * one_over_sin_omega
    result = Quarternion()
    result.w = k0*q0.w + k1*q1.w
    result.x = k0*q0.x + k1*q1.x
    result.y = k0*q0.y + k1*q1.y
    result.z = k0*q0.z + k1*q1.z
    return result 
def conjugate(q: Quarternion) -> Quarternion:
    result = Quarternion() 
    # same rotation amount
    result.w = q.w
    # opposite axis 
    result.x = -q.x 
    result.y = -q.y
    result.z = -q.z 
    return result
def pow(q: Quarternion, exponent: float) -> Quarternion:
    if abs(q.w) >0.999:
        # identity quaternion
        return q 
    result = Quarternion()
    alpha = math.acos(q.w)    # half angle 
    new_alpha = alpha * exponent  
    result.w = math.cos(new_alpha)
    mult = math.sin(new_alpha) / math.sin(alpha) # chnage in half angle
    result.x = q.x * mult 
    result.y = q.y * mult 
    result.z = q.z * mult 
    return result 