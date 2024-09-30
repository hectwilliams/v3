import vector3
# import euler_angles
import quarternion
import rotation_matrix
import numpy as np 


class Matrix4x3():
    def __init__(self):
        self.m11 = np.float32(0)
        self.m12 = np.float32(0)
        self.m13 = np.float32(0)
        self.m21 = np.float32(0)
        self.m22 = np.float32(0)
        self.m23 = np.float32(0)
        self.m31 = np.float32(0)
        self.m32 = np.float32(0)
        self.m33 = np.float32(0)
        self.tx =  np.float32(0)
        self.ty =  np.float32(0)
        self.tz =  np.float32(0)
        self.identity()
    def __repr__(self) -> str:
        return (f'self.m11={self.m11} self.m12={self.m12} self.m13={self.m13}\n' 
                f'self.m21={self.m21} self.m22={self.m22} self.m23={self.m23}\n'
                f'self.m31={self.m31} self.m32={self.m32} self.m33={self.m33}\n'
                f'self.tx={self.tx} self.ty={self.ty} self.tz={self.tz}\n'
                )
    def identity(self):
        self.m11 = 1.0; self.m12 = 0.0; self.m13 = 0.0 
        self.m21 = 0.0; self.m22 = 1.0; self.m23 = 0.0 
        self.m31 = 0.0; self.m32 = 0.0; self.m33 = 1.0
        self.tx = 0.0;  self.ty = 0.0;  self.tz = 0.0 
    def zero_translation(self):
        self.tx = self.ty = self.tz = 0.0 
    def set_translation(self, d: vector3.Vector3):
        self.tx = d.x
        self.ty = d.y 
        self.tz = d.z 
    def setup_translation(self, d: vector3.Vector3):
        self.m11 = 1.0; self.m12 = 0.0; self.m13 = 0.0
        self.m21 = 0.0; self.m22 = 1.0; self.m23 = 0.0
        self.m31 = 0.0; self.m32 = 0.0; self.m33 = 1.0
        self.tx = d.x 
        self.ty = d.y 
        self.tz = d.z
    def setup_local_parent_euler(self, pos: vector3.Vector3, orient)->None:
        """ create a rotation matrix
            matrix to perform a local -> parent transformation (e.g. inertial -> object)
        Args:
            pos - vector3.Vector3
            orient - euler_angles.EulerAngles
        """
        # creation rotation matrix
        orient_matrix = rotation_matrix.RotationMatrix()
        orient_matrix.setup(orient)
        # setup 4x3 matrix
        self.setup_local_to_parent_matrix(pos, orient_matrix)
    def setup_local_to_parent_matrix(self, pos, orient)->None:
        """ matrix to perform a local -> parent transformation,
            normal rotation matrix convention is  inertial-> object (parent->local); we want object->interial (local -> parent) so transpose matrix 
        Args:
            pos - vector3.Vector3
            orient - rotation_matrix.RotationMatrix
        """
        # copy tranposed 3x3 matrix portion
        self.m11 = orient.m11; self.m12 = orient.m21; self.m13 = orient.m31
        self.m21 = orient.m12; self.m22 = orient.m22; self.m23 = orient.m32
        self.m31 = orient.m13; self.m32 = orient.m23; self.m33 = orient.m33
        # translation happens after 3x3 matrix portion
        self.tx = pos.x 
        self.ty = pos.y 
        self.tz = pos.z 
    def setup_parent_to_local_euler(self, pos, orient)->None:
        """ create a rotation matrix
            matrix to perform a world -> object 
        Args:
            pos - vector3.Vector3
            orient - euler_angles.EulerAngles
        """
        orient_matrix = rotation_matrix.RotationMatrix()
        orient_matrix.setup(orient)
        self.setup_parent_to_local_matrix(pos, orient_matrix)
    def setup_parent_to_local_matrix(self, pos, orient)->None:
        """
            matrix to perform a world -> object 
        Args:
            pos - vector3.Vector3
            orient - rotation_matrix.RotationMatrix
        """
        # copy the rotation matrix
        self.m11 = orient.m11, self.m12=orient.m12, self.m13=orient.m13
        self.m21 = orient.m21, self.m22=orient.m22, self.m23=orient.m23
        self.m31 = orient.m31, self.m32=orient.m32, self.m33=orient.m33
        # rotation occurs first; we must correct for that by rotating the translation portion ( i.e. T_vector * R_matrix ) 
        self.tx = -(pos.x*self.m11 + pos.y*self.m21 + pos.z*self.m31)
        self.ty = -(pos.x*self.m12 + pos.y*self.m22 + pos.z*self.m32)
        self.tz = -(pos.x*self.m13 + pos.y*self.m23 + pos.z*self.m33)
    def setup_rotate_cardinal(self, axis: int, theta: float):
        """
            setup matrix to perform a rotation about cardinal axis

            Args:
                axis - axis of rotation 
                1 => rotate  about the x-axis
                2 => rotate  about the y-axis
                3 => rotate  about the z-axis
        """
        c_axis, s_axis = cos_sin(theta)
        if axis == 1:
            # rotate about x-axis 
            self.m11 = 1.0; self.m12 = 0.0; self.m13 = 0.0 
            self.m21 = 0.0; self.m22 = c_axis; self.m23 = s_axis
            self.m31 = 0.0; self.m32 = -s_axis; self.m33 = c_axis 
        elif axis == 2:
            # rotate about y-axis
            self.m11 = c_axis; self.m12 = 0.0; self.m13 = -s_axis
            self.m21 = 0.0; self.m22 = 1.0; self.m23 = 0.0
            self.m31 = s_axis; self.m32 = 0.0; self.m33 = c_axis
        elif axis == 3:
            # rotate about z-axis 
            self.m11 = c_axis; self.m12 = s_axis; self.m13 = 0.0
            self.m21 = -s_axis; self.m22 = c_axis; self.m23 = 0.0
            self.m31 = 0.0; self.m32 = 0.0; self.m33 = 1.0
        self.tx = self.ty = self.tz = 0.0
    def setup_rotate_arbitrary(self, axis: vector3.Vector3, theta: np.float64):
        """
            setup matrix to perform a rotation about arbitrary axis
        """
        assert(abs(axis*axis - 1.0) < 0.01) # unit vector sanity check 
        cos, sin = cos_sin(theta)
        self.m11 = axis.x*axis.x * (1- cos) + cos
        self.m12 = axis.x*axis.y * (1 - cos) + axis.z*sin
        self.m13 = axis.x*axis.z * (1 - cos) - axis.y*sin
        self.m21 = axis.x*axis.y * (1 - cos) - axis.z*sin
        self.m22 = axis.y*axis.y * (1 - cos) + cos
        self.m23 = axis.y*axis.z * (1- cos) + axis.x*sin
        self.m31 = axis.x*axis.z * (1 - cos) + axis.y*sin 
        self.m32 = axis.y*axis.z * (1 - cos) - axis.x*sin
        self.m33 = axis.z*axis.z * (1 - cos) + cos
        self.tx = self.ty = self.tz = 0
    def from_quarternion(self, q):
        """
            setup matrix to perform rotation, given the angular displacement
        Args:
            q - quarternion.Quarternion
        """
        ww = np.float64(2.0) * q.w 
        xx = np.float64(2.0) * q.x 
        yy = np.float64(2.0) * q.y 
        zz = np.float64(2.0) * q.z
        self.m11 = np.float64(1.0) - yy*q.y - zz*q.z
        self.m12 = xx*q.y + ww*q.z
        self.m13 = xx*q.z - ww*q.x
        self.m21 = xx*q.y - ww*q.z
        self.m22 = np.float64(1.0) - xx*q.x - zz*q.z 
        self.m23 = yy*q.z + ww*q.x
        self.m31 = xx*q.z + ww*q.y
        self.m32 = yy*q.z - ww*q.x 
        self.m33 = np.float64(1.0) - xx*q.x - yy*q.y
        self.tx = self.ty = self.tz = 0.0
    def setup_scale(self, v):
        """
            setup matrix to perform scale on each axis
        """
        self.m11 = v.x 
        self.m12 = 0.0 
        self.m13 = 0.0 

        self.m21 = 0.0 
        self.m22 = v.y 
        self.m23 = 0.0 

        self.m31 = 0.0 
        self.m32 = 0.0 
        self.m33 = v.z 

        self.tx = self.ty = self.tz = 0.0
    def setup_scale_along_axis(self, axis: vector3.Vector3, k: float):
        """
            setup scale to perform scale along an arbitrary axis
        """
        assert( (abs(axis*axis) - 1.0) < 0.01)
        self.m11 = 1 + (k - 1)*axis.x*axis.x
        self.m12 = (k - 1)*axis.x*axis.y
        self.m13 = (k - 1)*axis.x*axis.z 
        self.m21 = (k - 1)*axis.x*axis.y
        self.m22 = 1 + (k - 1)*axis.y*axis.y
        self.m23 = (k - 1)*axis.y*axis.z 
        self.m31 = (k - 1)*axis.x*axis.z
        self.m32 = (k - 1)*axis.y*axis.z 
        self.m33 = 1 + (k - 1)*axis.z*axis.z
        self.tx = self.ty = self.tz = 0.0 
    def setup_shear(self,axis, s: float, t: float):
        """
            setup matrix to perform a shear

            shear specified by 1-based 'axis' index
            axis == 1  =>  y += s*x, z += t*x
            axis == 2  =>  x += s*y, z += t*y
            axis == 3  =>  x += s*z, y += t*z

        """    
        if axis == 1:
            self.m11 = 1.0; self.m12 = s;   self.m13 = t 
            self.m21 = 0.0; self.m22 = 1.0; self.m23 = 0.0 
            self.m31 = 0.0; self.m32 = 0.0; self.m33 = 1.0
        elif axis == 2:
            self.m11 = 1.0; self.m12 = 0.0; self.m13 = 0.0
            self.m21 = s;   self.m22 = 1.0; self.m23 = t
            self.m31 = 0.0; self.m32 = 0.0; self.m33 = 1.0
        elif axis == 3:
            self.m11 = 1.0; self.m12 = 0.0; self.m13 = 0.0 
            self.m21 = 0.0; self.m22 = 1.0; self.m23 = 0.0 
            self.m31 = s;   self.m32 = t;   self.m33 = 1.0 
        else:
            assert(False)
        self.tx = self.ty = self.tz = 0.0
    def setup_project(self, n: vector3.Vector3):
        """setup projection onto a plane passing through origin"""
        assert( abs(n*n - 1.0) < 0.01 )
        self.m11 = 1.0 - n.x*n.x 
        self.m22 = 1.0 - n.y*n.y 
        self.m33 = 1.0 - n.z*n.z 
        self.m12 = self.m21 = -n.x*n.y 
        self.m13 = self.m31 = -n.x*n.z 
        self.m23 = self.m32 = -n.y*n.z
        self.tx = self.ty = self.tz = 0.0 
    def setup_reflect_about_place(self, axis:int, k: float):
        """
            setup matrix to perform a reflection about a plane parralel to to cardinal plane
            axis is 1 based index, which specifies the plane to project aboue
                1: reflect aboout the x=k plane 
                2: reflect about the x=k plane 
                3: reflect about the x=k plane 
        """
        if axis == 1:
            # reflect about the plane x=k
            self.m11 = -1.0; self.m12 = 0.0; self.m13 = 0.0
            self.m21 = 0.0;  self.m22 = 1.0; self.m23 = 0.0
            self.m31 = 0.0;  self.m32 = 0.0; self.m33 = 1.0
            self.tx = 2.0 * k 
            self.ty = 0.0 
            self.tz = 0.0 
        elif axis == 2:
            # reflect about the plane y=k
            self.m11 = 1.0; self.m12 = 0.0;  self.m13 = 0.0 
            self.m21 = 0.0; self.m22 = -1.0; self.m23 = 0.0 
            self.m31 = 0.0; self.m32 = 0.0;  self.m33 = 1.0
            self.tx = self.tz = 0.0
            self.ty = 2.0 * k
        elif axis == 3:
            # reflect about the plane z=k
            self.m11 = 1.0; self.m12 = 0.0; self.m13 = 0.0 
            self.m21 = 0.0; self.m22 = 1.0; self.m23 = 0.0 
            self.m31 = 0.0; self.m32 = 0.0; self.m33 = -1.0
            self.tx = 0.0 
            self.ty = 0.0 
            self.tz = 2.0 * k
        else :
            assert(False)
    def setup_reflect_arbitrary(self, n: vector3.Vector3):
        """
            setup matrix to perform a reflection about a arbritrary axis
        """
        # assert(abs(n*n -1.0) < 0.0001)
        self.m11 = 1.0- 2.0*n.x*n.x 
        self.m12 = -2.0*n.x*n.y
        self.m13 = -2.0*n.x*n.y
        self.m21 = -2.0*n.x*n.y
        self.m22 = 1.0 - 2.0*n.y
        self.m23 = -2.0*n.y*n.z 
        self.m31 = -2*n.x*n.z 
        self.m32 = -2.0*n.y*n.z 
        self.m33 = 1.0 - 2.0*n.z*n.z
        self.tx = self.ty = self.tz = 0.0 
    def to_numpy(self) ->np.ndarray:
        """
            get numpy type array
        """
        return np.array([
            [self.m11, self.m12, self.m13],
            [self.m21, self.m22, self.m23],
            [self.m31, self.m32, self.m33],
            ]
        )
    
    def to_numpy_4x3(self) ->np.ndarray:
        """
            get numpy type array
        """
        return np.array([
            [self.m11, self.m12, self.m13],
            [self.m21, self.m22, self.m23],
            [self.m31, self.m32, self.m33],
            [self.tx, self.ty, self.tz],
            ]
        )
def vector_mult(p: vector3. Vector3, m: Matrix4x3)->vector3.Vector3:
    """ vector * matrix"""
    return vector3.Vector3(
        p.x*m.m11 + p.y*m.m21 + p.z*m.m31 + m.tx,
        p.x*m.m12 + p.y*m.m22 + p.z*m.m32 + m.ty,
        p.x*m.m13 + p.y*m.m23 + p.z*m.m33 + m.tz
    )
def matrix_concat(a: Matrix4x3, b: Matrix4x3)-> Matrix4x3:
    r = Matrix4x3() 
    r.m11 = a.m11*b.m11 + a.m12*b.m21 + a.m13*b.m31
    r.m12 = a.m11*b.m12 + a.m12*b.m22 + a.m13*b.m32
    r.m13 = a.m11*b.m13 + a.m12*b.m23 + a.m13*b.m33

    r.m21 = a.m21*b.m11 + a.m22*b.m21 + a.m23*b.m31 
    r.m22 = a.m21*b.m12 +a.m22*b.m22 + a.m23*b.m32 
    r.m23 = a.m21*b.m13 + a.m22*b.m23 + a.m23*b.m33 

    r.m31 = a.m31*b.m11 + a.m32*b.m21 + a.m33*b.m31 
    r.m32 = a.m31*b.m12 + a.m32*b.m22 + a.m33*b.m32 
    r.m33 = a.m31*b.m13 + a.m32*b.m23 + a.m33*b.m33 

    r.tx = a.tx*b.m11 + a.ty*b.m21 + a.tz*b.m31 + b.tx
    r.ty = a.tx*b.m12 + a.ty*b.m22 + a.tz*b.m32 + b.ty
    r.tz = a.tx*b.m13 + a.ty*b.m23 + a.tz*b.m33 + b.tz
    return r
def determinant(m: Matrix4x3) ->float: 
    return m.m11*(m.m22*m.m33 - m.m23*m.m32) + m.m12*(m.m23*m.m31 - m.m21*m.m33) + m.m13*(m.m21*m.m32 - m.m22*m.m31)
def inverse (m: Matrix4x3):
    det = determinant(m)
    assert(abs(det) <= 0.0001) # singular/ non-invertible matrix 
    one_over_det = 1.0 / det 
    r = Matrix4x3()
    r.m11 = (m.m22*m.m33 - m.m23*m.m32) * one_over_det
    r.m12 = (m.m13*m.m32 - m.m12*m.m33) * one_over_det
    r.m13 = (m.m12*m.m23 - m.m13*m.m22) * one_over_det

    r.m21 = (m.m23*m.m31 - m.m21*m.m33) * one_over_det
    r.m22 = (m.m11*m.m33 - m.m13*m.m31) * one_over_det
    r.m23 = (m.m13*m.m21 - m.m11*m.m23) * one_over_det

    r.m31 = (m.m21*m.m32 - m.m22*m.m31) * one_over_det
    r.m32 = (m.m12*m.m31 - m.m11*m.m32) * one_over_det
    r.m33 = (m.m11*m.m22 - m.m12*m.m21) * one_over_det

    r.tx = -(m.tx*r.m11 + m.ty*r.m21 + m.tz*r.m31)
    r.ty = -(m.tx*r.m12 + m.ty*r.m22 + m.tz*r.m32)
    r.tz = -(m.tx*r.m13 + m.ty*r.m23 + m.tz*r.m33)
    return r
def get_translation(m: Matrix4x3)->vector3.Vector3:
    return vector3.Vector3(m.tx, m.ty, m.tz)
def get_position_from_parent_local_matrix(m: Matrix4x3)-> vector3.Vector3:
    """ extract position of an object given a parent -> local transformation matrix (e.g. world -< object matrix)"""
    return vector3.Vector3(
        -(m.tx*m.m11 + m.ty*m.m12 + m.tz*m.m13),
        -(m.tx*m.m21 + m.ty*m.m22 + m.tz*m.m23),
        -(m.tx*m.m31 + m.ty*m.m32 + m.tz*m.m33)
    )
def get_position_from_local_to_parent_matrix(m: Matrix4x3)->vector3.Vector3:
    """extract position of an object given a local -> pareent transformation (e.g. object -> world matrix)"""
    return vector3.Vector3(m.tx, m.ty, m.tz)
def cos_sin(theta: float) -> tuple:
    """Compute sin and cos angle for quaternion."""
    return math.cos(theta), math.sin(theta)