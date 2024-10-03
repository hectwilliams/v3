""" Bounding Box """
import matplotlib.axes
import numpy as np 
import vector3
import matplotlib.pyplot as plt 
import matplotlib
import matrix_4x3
from  mpl_toolkits.mplot3d.art3d import Line3D, Line3DCollection

LINE_MAP = [ [0,1], [1,3], [2,3], [0,2],[0,4], [4,6], [2,6], [4,5],[6,7],[5,7],[1,5],[5,7],[3,7],[1,3]]
class AABB():
    def __repr__(self) -> str:
        return ('{}\n{}\n').format(self.vmax, self.vmin)
    def __init__(self) -> None:
        self.vmin = vector3.Vector3()
        self.vmax = vector3.Vector3()
        self.box_vertices = np.array([vector3.Vector3() for _ in range(8)])
        self.plot_buffer = [matplotlib.axes.Axes for _ in range(len(LINE_MAP))]
        self.vsize = np.zeros((3))
        self.center = np.zeros((3))
        self.is_on = False
        self.faces = {
            'xz': {'ymin': {'center': vector3.Vector3, 'n': vector3.Vector3, 'plot': plt.quiver }, 'ymax': {'center': vector3.Vector3, 'n': vector3.Vector3, 'plot': plt.quiver }  },
            'xy': {'zmin': {'center': vector3.Vector3, 'n': vector3.Vector3, 'plot': plt.quiver }, 'zmax': {'center': vector3.Vector3, 'n': vector3.Vector3, 'plot': plt.quiver }  },
            'yz': {'xmin': {'center': vector3.Vector3, 'n': vector3.Vector3, 'plot': plt.quiver }, 'xmax': {'center': vector3.Vector3, 'n': vector3.Vector3, 'plot': plt.quiver }  },
        }
        self.empty()
    # def intersection_ray_plane(self, plane_normal: np.ndarray, pts_on_plane: vector3.Vector3):
    #     for plane ,a ,b  in [  ('xz', 'ymin' , 'ymax'), ('xy', 'zmin' , 'zmax') , ('yz', 'xmin' , 'xmax') ]:
    #         for side in [a,b]:
    #             c = self.faces[plane][side]['center']
    #             n = self.faces[plane][side]['n']
                

    #             d_norm = rng.random(size=(3)) #direction of po
    #             po_dot_n = po.to_numpy().dot(normal)
    #             d_dot_n = d_norm.dot(normal)
    #             t = (d - po_dot_n) / d_dot_n
    #             po_intersect = po.to_numpy() + t*d_norm
                
    def empty(self)-> None:
        big_number = np.finfo(np.float16).max
        self.vmax.x = self.vmax.y = self.vmax.z = -big_number
        self.vmin.x = self.vmin.y = self.vmin.z = big_number
    def is_empty(self)->bool:
        if (self.vmin.x > self.vmax.x) | (self.vmin.y > self.vmax.y) | (self.vmin.z > self.vmax.z):
            return True 
        return False 
    def acquire(self, data: np.ndarray, axis = 0):
        """Set vmin vmax. Function is used to initialize the boudning box with a static points prior to any tranformations"""
        if axis == 0:
            if data.min() < self.vmin.x:
                self.vmin.x = data.min()
            if data.max() > self.vmax.x:
                self.vmax.x = data.max()
        elif axis == 1:
            if data.max()> self.vmax.y:
                self.vmax.y = data.max()
            if data.min()< self.vmin.y:
                self.vmin.y = data.min()
        elif axis == 2:
            # print(axis, data.min(), data.max())
            if data.max() > self.vmax.z:
                self.vmax.z = data.max()

            if data.min()< self.vmin.z:
                self.vmin.z = data.min()
        self.size = self.vmax - self.vmin
        self.center = (self.vmax + self.vmin)/2
    def xform(self, m: matrix_4x3.Matrix4x3, ax):
        for i in range(self.box_vertices.size):
            self.box_vertices[i] = matrix_4x3.vector_mult(self.box_vertices[i], m)
    def box(self, ax):
        self.remove_box()
        """draw bounding box"""
        for i in range(len(LINE_MAP)):
            i_a = LINE_MAP[i][0]
            i_b = LINE_MAP[i][1]
            v_a = self.box_vertices[i_a]
            v_b = self.box_vertices[i_b]
            self.plot_buffer[i] = ax.plot( [v_a.x, v_b.x] , [v_a.y, v_b.y], [v_a.z, v_b.z] , c='black', alpha=0.3)
        self.is_on = True
    def remove_box(self):
        if self.is_on:
            for i in range(len(LINE_MAP)):
                for l in self.plot_buffer[i]:
                    l.remove() 
        self.is_on = False
    def toggle_touch_points(self, ax):
        if self.is_empty():
            return 
        """center normals on each side of box"""
        for plane ,a ,b  in [  ('xz', 'ymin' , 'ymax'), ('xy', 'zmin' , 'zmax') , ('yz', 'xmin' , 'xmax') ]:
            for side in [a,b]:
                c = self.faces[plane][side]['center']
                n = self.faces[plane][side]['n']
                plt_status = self.faces[plane][side]['plot'] 
                # print(plt_status, c, n)
                if not isinstance(plt_status, Line3DCollection):
                    self.faces[plane][side]['plot'] =   ax.quiver(*c, *n, linewidth = 1, arrow_length_ratio=0.1 )  
                    # = ax.plot(*zip(c.to_numpy(), n))
                else:
                    self.faces[plane][side]['plot'].remove()
                    # for line in self.faces[plane][side]['plot']:
                        # line.remove()
    def enable_touch_points(self, ax):
        face_normals(self.vmin, self.vmax, self.faces, ax)
        for plane ,a ,b  in [  ('xz', 'ymin' , 'ymax'), ('xy', 'zmin' , 'zmax') , ('yz', 'xmin' , 'xmax') ]:
            for side in [a,b]:
                c = self.faces[plane][side]['center']
                n = self.faces[plane][side]['n']
                self.faces[plane][side]['plot'] =   ax.quiver(*c, *n, linewidth = 1, arrow_length_ratio=0.1 )  

    def remove_touch_points(self):
        if self.is_empty():
            return 
        for plane ,a ,b  in [  ('xz', 'ymin' , 'ymax'), ('xy', 'zmin' , 'zmax') , ('yz', 'xmin' , 'xmax') ]:
            for side in [a,b]:
                ele = self.faces[plane][side]['plot']
                if hasattr(ele, 'remove'):
                    print(ele)
                    ele.remove()                
                    
    def update_box(self, pts, ax) ->None:
        self.empty()
        data = np.array(list(map(lambda pt: [pt.x, pt.y, pt.z], pts ))).T
        self.acquire(data[0], 0)
        self.acquire(data[1], 1)
        self.acquire(data[2], 2)
        set_vertices(self.vmin, self.vmax, self.box_vertices) # 8 points required for bbox toggle_touch_points
        self.box(ax)
def face_normals(vmin, vmax, faces, ax):
    # xz - ymin
    v1 = vector3.Vector3(vmin.x, vmin.y, vmin.z)
    v2 = vector3.Vector3(vmin.x, vmin.y, vmax.z)
    v3 = vector3.Vector3(vmax.x, vmin.y, vmax.z)
    v4 = vector3.Vector3(vmax.x, vmin.y, vmin.z)
    e2 = v2 - v1 
    e1 = v3 - v1 
    e2xe1 = np.cross(e1.to_numpy(), e2.to_numpy())
    n = e2xe1 #/ np.linalg.norm(e2xe1)
    center = (v1 + v2 + v3 + v4) / 4
    faces['xz']['ymin']['center'] =  center
    faces['xz']['ymin']['n'] =  n
    # ax.plot(*zip(center.to_numpy(), n))
    # ax.scatter(*n, s=5, color='red')
    
    # xz - ymax
    v1 = vector3.Vector3(vmin.x, vmax.y, vmin.z)
    v2 = vector3.Vector3(vmin.x, vmax.y, vmax.z)
    v3 = vector3.Vector3(vmax.x, vmax.y, vmax.z)
    v4 = vector3.Vector3(vmax.x, vmax.y, vmin.z)

    e2 = v2 - v3 
    e1 = v1 - v2 
    e2xe1 = np.cross(e1.to_numpy(), e2.to_numpy())
    n = e2xe1 #/ np.linalg.norm(e2xe1)
    center = (v1 + v2 + v3 + v4) / 4
    faces['xz']['ymax']['center'] =  center
    faces['xz']['ymax']['n'] =  n

    # xy - ymin
    v1 = vector3.Vector3(vmin.x, vmin.y, vmin.z)
    v2 = vector3.Vector3(vmin.x, vmax.y, vmin.z)
    v3 = vector3.Vector3(vmax.x, vmax.y, vmin.z)
    v4 = vector3.Vector3(vmax.x, vmin.y, vmin.z)
    e2 = v2 - v3
    e1 = v1 - v2
    e2xe1 = np.cross(e1.to_numpy(), e2.to_numpy())
    n = e2xe1 #/ np.linalg.norm(e2xe1)
    center = (v1 + v2 + v3 + v4) / 4
    faces['xy']['zmin']['center'] =  center
    faces['xy']['zmin']['n'] =  n
    
    # xy - ymax
    v1 = vector3.Vector3(vmin.x, vmin.y, vmax.z)
    v2 = vector3.Vector3(vmin.x, vmax.y, vmax.z)
    v3 = vector3.Vector3(vmax.x, vmax.y, vmax.z)
    v4 = vector3.Vector3(vmax.x, vmin.y, vmax.z)
    e2 = v2 - v1
    e1 = v3 - v2
    e2xe1 = np.cross(e1.to_numpy(), e2.to_numpy())
    n = e2xe1 #/ np.linalg.norm(e2xe1)
    center = (v1 + v2 + v3 + v4) / 4
    faces['xy']['zmax']['center'] =  center
    faces['xy']['zmax']['n'] =  n

    # yz - xmax
    v1 = vector3.Vector3(vmax.x, vmin.y, vmin.z)
    v2 = vector3.Vector3(vmax.x, vmin.y, vmax.z)
    v3 = vector3.Vector3(vmax.x, vmax.y, vmax.z)
    v4 = vector3.Vector3(vmax.x, vmax.y, vmin.z)
    e2 = v2 - v1
    e1 = v3 - v2
    e2xe1 = np.cross(e1.to_numpy(), e2.to_numpy())
    n = e2xe1 #/ np.linalg.norm(e2xe1)
    center = (v1 + v2 + v3 + v4) / 4
    faces['yz']['xmax']['center'] =  center
    faces['yz']['xmax']['n'] =  n

    # yz - xmin
    v4 = vector3.Vector3(vmin.x, vmin.y, vmin.z)
    v3 = vector3.Vector3(vmin.x, vmin.y, vmax.z)
    v2 = vector3.Vector3(vmin.x, vmax.y, vmax.z)
    v1 = vector3.Vector3(vmin.x, vmax.y, vmin.z)
    e2 = v2 - v1
    e1 = v3 - v2
    e2xe1 = np.cross(e1.to_numpy(), e2.to_numpy())
    n = e2xe1 #/ np.linalg.norm(e2xe1)
    center = (v1 + v2 + v3 + v4) / 4
    faces['yz']['xmin']['center'] =  center
    faces['yz']['xmin']['n'] =  n 
    # ax.plot(*zip(center.to_numpy(), n))
    # ax.scatter(*n, s=5, color='red')

def set_vertices(vmin, vmax, vertcies):
    """ using vmax and vmax vector assign 8 points for bounding box"""
    #0
    vertcies[0].x = vmin.x
    vertcies[0].y = vmin.y 
    vertcies[0].z = vmin.z

    #1
    vertcies[1].x = vmax.x 
    vertcies[1].y = vmin.y 
    vertcies[1].z = vmin.z

    #2 
    vertcies[2].x = vmin.x 
    vertcies[2].y = vmin.y 
    vertcies[2].z = vmax.z

    #3 
    vertcies[3].x = vmax.x 
    vertcies[3].y = vmin.y 
    vertcies[3].z = vmax.z 

    #4 
    vertcies[4].x = vmin.x 
    vertcies[4].y = vmax.y 
    vertcies[4].z = vmin.z 

    #5 
    vertcies[5].x = vmax.x 
    vertcies[5].y = vmax.y 
    vertcies[5].z = vmin.z 

    #6 
    vertcies[6].x = vmin.x 
    vertcies[6].y = vmax.y 
    vertcies[6].z = vmax.z 
    
    #7 
    vertcies[7].x = vmax.x 
    vertcies[7].y = vmax.y 
    vertcies[7].z = vmax.z 