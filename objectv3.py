"""Operations on Object created using vectors """
import vector3
import matrix_4x3
import numpy as np 
import aabb3
import time
class Objectv3():
    def __init__(self, center= np.zeros(shape=(3)), axes = None) -> None:
        self.pts = np.array([vector3.Vector3(0, 0,0)  for _ in range( 3 ) ])
        self.axes = axes
        self.axes_pad = None 
        self.bbox = aabb3.AABB()
        self.center = center
    def add_collection(self, vertices):
        number_of_vertices = len(vertices)
        self.pts = np.array([vector3.Vector3  for _ in range( len(number_of_vertices)) ])
        for i in range(number_of_vertices):
            self.pts[i] = vertices[i]
    def load_mesh(self, xx_flatten, yy_flatten, zz_flatten):
        """load flattened xx, yy, zz meshgrid data. This method r equires object to have a zero vector origin"""
        self.pts = np.array([vector3.Vector3  for _ in range(len(xx_flatten) ) ])
        for index in range(self.pts.size):
            self.pts[index] = self.pts[index](xx_flatten[index], yy_flatten[index], zz_flatten[index])
    def set_axes(self, ax):
        self.axes = ax
    def show(self, ax, kwags = {} ):
        self.axes = ax
        self.axes_pad = ax.scatter(*np.array(list(map(lambda pt: [pt.x, pt.y, pt.z], self.pts ))).T, s=0.5, **kwags)
        self.bbox.update_box(self.pts, self.axes)
    def unshow(self):
        if self.axes_pad:
            self.bbox.remove_box() # is there a way to hide the lines (hide method ?)
            self.axes_pad.remove()
    def xform(self, m: matrix_4x3.Matrix4x3):
        for i in range(self.pts.size):
            self.pts[i] = matrix_4x3.vector_mult(self.pts[i], m)
    def plot_point(self, v, ax, c= None):
        ax.scatter(v.x, v.y, v.z, marker='o', s= 1, c = 'black' if c== None else c)
    def show_bbox(self):
        if self.axes == None:
            raise TypeError('BOX ERROR')
        # self.bbox.update_box(self.pts, self.axes)
    def remove_bbox(self):
        self.bbox.remove_box() # is there a way to hide the lines (hide method ?)
    def intersect_bbox_test(self, obj, obj_id = 0):
        """ does test_object intersect current box
        
        Args:
            obj - test object to bouding box

        Returns:
            tuple containing np_array of obj pts projected(closests points) onto bounding box 
        """
        if not self.bbox.is_on:
            raise RuntimeError('bounding box not enabled')
        c = obj.center.copy()
        test = False 
        for i in range(obj.pts.size):
            if obj.pts[i].x < self.bbox.vmin.x:
                c[0] = self.bbox.vmin.x
            elif obj.pts[i].x > self.bbox.vmax.x:
                c[0] = self.bbox.vmax.x
            if obj.pts[i].y < self.bbox.vmin.y:
                c[1] = self.bbox.vmin.y
            elif obj.pts[i].y > self.bbox.vmax.y:
                c[1] = self.bbox.vmax.y
            if obj.pts[i].z < self.bbox.vmin.z:
                c[2] = self.bbox.vmin.z
            elif obj.pts[i].z > self.bbox.vmax.z:
                c[2] = self.bbox.vmax.z
        d = np.linalg.norm((c - obj.center).to_numpy(), ord=2)
        # sphere
        if obj_id == 0:
            print(f'distance={d}\tradius={obj.r}')
            test = d < obj.r
        return c, test
        
def center_of_gravity(pts):
    v = vector3.Vector3(0,0,0)
    for v_ele in pts:
        v = v + v_ele
    return np.divide(v, np.float32(len(pts)) ) 
def err_vector(v1, v2, size):
    return np.sum(np.square(v2-v1))/(size)

def normalize(n: vector3.Vector3):
    n = n.to_numpy()
    mag = np.linalg.norm(n)
    n_dot_n = mag**2.0
    if np.abs(n_dot_n - 1.0) > 0.01:
        for i in range(n.size):
            n[i] = n[i]/mag
    return vector3.Vector3(*n)
