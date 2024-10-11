"""Operations on Object created using vectors """
import vector3
import matrix_4x3
import aabb3
import matplotlib.pyplot as plt 
import time 
import numpy as np
from  mpl_toolkits.mplot3d.art3d import Line3D
import quarternion

class Objectv3():
    def __init__(self, center= vector3.Vector3(), axes= any) -> None:
        self.pts = np.array([vector3.Vector3(0, 0,0)  for _ in range( 3 ) ])
        self.axes = axes
        self.axes_pad = None 
        self.bbox = aabb3.AABB(axes)
        self.center = center

    def add_collection(self, vertices):
        number_of_vertices = len(vertices)
        self.pts = np.array([vector3.Vector3  for _ in range( len(number_of_vertices)) ])
        for i in range(number_of_vertices):
            self.pts[i] = vertices[i]
    def load_mesh(self, xx_flatten, yy_flatten, zz_flatten):
        """load flattened xx, yy, zz meshgrid data. This method r equires object to have a zero vector origin"""
        length_ = len(xx_flatten) 
        print(length_)
        self.pts = np.array( [vector3.Vector3()  for _ in range(length_) ] )
        for index in range(length_):
            self.pts[index] =  vector3.Vector3(xx_flatten[index], yy_flatten[index], zz_flatten[index])
    def set_axes(self, ax):
        self.axes = ax
    def show(self, hide_bbox=False, **kwags  ):
        """show vertices points"""
        data = np.array(list(map(lambda pt: pt.to_numpy(), self.pts)))
        self.axes_pad =  self.axes.scatter(*data.T, **kwags) # transpose to bucket each axis into x, y ,z parameters 
        self.bbox.update_box(self.pts, self.axes)
        if  hide_bbox:
            self.remove_bbox()
    def unshow(self):
        """remove vertices and bounding box"""
        if self.axes_pad:
            self.bbox.remove_box() # is there a way to hide the lines (hide method ?)
            self.axes_pad.remove()
        self.bbox.remove_touch_points()
    def xform(self, m: matrix_4x3.Matrix4x3):
        """transform/translate vertices"""
        xform_helper(self.pts, m)
        self.center= center_of_gravity(self.pts)
    def xform_q(self, q: quarternion.Quarternion ):
        m = matrix_4x3.Matrix4x3()
        m.from_quarternion(q)
        xform_helper(self.pts, m)
        self.center= center_of_gravity(self.pts)
    def show_bbox(self):
        if self.axes == None:
            raise TypeError('BOX ERROR')
    def remove_bbox(self):
        self.bbox.remove_box() # is there a way to hide the lines (hide method ?)

    def connect_vertices_plot(self, **kwargs):
        """Draw line connecting vertices
        
        Methods with _plot suffix follow matplotlib's axes.plot.kwargs dictionary structure
        """
        prev_ = -1
        next_ = 0
        

        condition = np.array(list(map(lambda v: True if v.z == 0 else False, self.pts)))
        contour_pts = np.extract( condition, self.pts)
        self.line_connect = [Line3D for _ in range(contour_pts.size)] 
        
        # sort circle of points on plane to create ordered points which create a loop
        # dataset_pts = sorted(dataset_pts, key=lambda v_pt:  v_pt.y )
        
        len_over_2 = int(contour_pts.size/2)
        contour_pts = np.array(sorted(contour_pts.tolist(), key=lambda v_pt:  np.atan2(v_pt.y , v_pt.x) ))
        
            # print(dataset_pts)xs
        for i in range (contour_pts.size):
            self.line_connect[i] = self.axes.plot(*zip(contour_pts[prev_].to_numpy(), contour_pts[next_].to_numpy())  , **kwargs)
            prev_ = next_
            next_ = prev_ + 1

    def disconnect_vertices(self):
        if hasattr(self, 'line_connect'):
            for lines in self.line_connect:
                for line in lines:
                    line.remove()
            self.line_connect = None
            del self.line_connect
    def toggle_vertices(self):
        if self.axes_pad:
            current_state = self.axes_pad.get_visible()
            self.axes_pad.set_visible(not current_state)
    
    def toggle_connect_line(self):
        if hasattr(self, 'line_connect'):
            for lines in self.line_connect:
                for line in lines:
                    curr_state = line.get_visible()
                    line.set_visible(not curr_state)
            self.line_connect = None 
            del self.line_connect
        else:
            self.connect_vertices_plot(c='black')
    def toggle_bbox(self):
        self.bbox.toggle_box()
    
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
    return vector3.Vector3(*np.divide(v, np.float32(len(pts)) ) )

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

def xform_helper( pts, m : matrix_4x3.Matrix4x3):
    """ helper for .xform methold above, performs vector tranform/translate operations"""
    for i in range(pts.size):
        pts[i] = matrix_4x3.vector_mult(pts[i], m)