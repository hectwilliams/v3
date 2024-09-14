"""Operations on Object created using vectors """
import vector3
import matrix_4x3
import numpy as np 
import aabb3

class Objectv3():

    def __init__(self, size_x= 50, size_y=50) -> None:
        self.xy_mesh_size = (size_x, size_y)
        self.center = vector3.Vector3(0,0,0) 
        self.pts = np.array([vector3.Vector3(0,0,0) ]*size_x*size_y*2)
        self.axes = None 
        self.rot_counter = np.int32(0)
        self.bbox = aabb3.AABB()
    def add_collection(self, vertices):
        assert( len(vertices) <= len(self.pts) )
        for i in range(len(vertices)):
            self.pts[i] = vertices[i]
        self.bbox.update_box(self.pts)
    def set_axes(self, ax):
        self.axes = ax
    def show(self, ax):
        self.axes = ax.scatter(*np.array(list(map(lambda pt: [pt.x, pt.y, pt.z], self.pts ))).T, c ='black', alpha=0.011)
    def unshow(self):
        if self.axes:
            self.axes.remove() 
    def xform(self, m: matrix_4x3.Matrix4x3, ax):
        for i in range(self.xy_mesh_size[0] * self.xy_mesh_size[1] ):
            self.pts[i*2] = matrix_4x3.vector_mult(self.pts[i*2], m)
            self.pts[i*2 + 1] = matrix_4x3.vector_mult(self.pts[i*2 +1], m)
        self.add_collection(self.pts)
        center = center_of_gravity(self.pts)  
        if ax:
            ax.scatter(center.x, center.y, center.z, s=1)
            self.bbox.rotate(m.to_numpy_4x3(), ax)
    def plot_point(self, v, ax, c= None):
        ax.scatter(v.x, v.y, v.z, marker='o', s= 1, c = 'black' if c== None else c)
def center_of_gravity(pts):
    v = vector3.Vector3(0,0,0)
    for v_ele in pts:
        v = v + v_ele
    return v/len(pts)
def err_vector(v1, v2, size):
    return np.sum(np.square(v2-v1))/(size)


