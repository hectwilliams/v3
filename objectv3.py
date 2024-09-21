"""Operations on Object created using vectors """
import vector3
import matrix_4x3
import numpy as np 
import aabb3
import time
class Objectv3():
    def __init__(self, n=50, center= np.zeros(shape=(3)), axes = None) -> None:
        self.pts = np.array([vector3.Vector3(0, 0,0)  for i in range( (n**2) *2 ) ])
        self.axes = axes
        self.axes_pad = None 
        self.bbox = aabb3.AABB()
        self.loaded_a_meshgrid = False
        self.center = center
        self.center_v = vector3.Vector3(*center)
        self.n = n
    def add_collection(self, vertices):
        assert( len(vertices) <= len(self.pts) )
        for i in range(len(vertices)):
            self.pts[i] = vertices[i]
    def load_mesh(self, xx, yy, zz):
        """load xx, yy, zz meshgrid data. This method requires object to have a zero vector origin"""
        n_sq = np.multiply(self.n,self.n) 
        for y_index in range( self.n ):
            for x_index in range( self.n ):
                index = self.n * y_index + x_index
                x = xx[y_index][x_index]
                y = yy[y_index][x_index]
                z = zz[y_index][x_index]
                v1 = vector3.Vector3( x,y,z)
                self.pts[index] = v1
                v2 = vector3.Vector3( -x, -y , -z)
                self.pts[index + n_sq ] = v2
    def set_axes(self, ax):
        self.axes = ax
    def show(self, ax, kwags = {} ):
        self.axes = ax
        self.axes_pad = ax.scatter(*np.array(list(map(lambda pt: [pt.x, pt.y, pt.z], self.pts ))).T, s=0.3, **kwags)
        self.bbox.update_box(self.pts, self.axes)
    def unshow(self):
        if self.axes_pad:
            self.bbox.remove_box() # is there a way to hide the lines (hide method ?)
            self.axes_pad.remove()
    def xform(self, m: matrix_4x3.Matrix4x3):
        for i in range(np.multiply(self.n,self.n)):
            self.pts[i*2] = matrix_4x3.vector_mult(self.pts[i*2], m)
            self.pts[i*2 + 1] = matrix_4x3.vector_mult(self.pts[i*2 +1], m)
        # self.bbox.xform(m, self.axes)
        # self.bbox.update_box(self.pts, self.axes)
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
        c = obj.center_v.copy()
        test = False 
        for i in range(obj.pts.size):
            if obj.pts[i].x < self.bbox.vmin.x:
                c.x = self.bbox.vmin.x
            elif obj.pts[i].x > self.bbox.vmax.x:
                c.x = self.bbox.vmax.x
            if obj.pts[i].y < self.bbox.vmin.y:
                c.y = self.bbox.vmin.y
            elif obj.pts[i].y > self.bbox.vmax.y:
                c.y = self.bbox.vmax.y
            if obj.pts[i].z < self.bbox.vmin.z:
                c.z = self.bbox.vmin.z
            elif obj.pts[i].z > self.bbox.vmax.z:
                c.z = self.bbox.vmax.z
        d = np.linalg.norm((c - obj.center_v).to_numpy(), ord=2)
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


