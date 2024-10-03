"""
    export PYTHONPATH="/Users/hectwilliams/Dev/v3:$PYTHONPATH"
"""
import numpy as np
import matplotlib.pyplot as plt 
import vector3
import time 
from  mpl_toolkits.mplot3d.art3d import Line3DCollection, Path3DCollection, Text3D, Line3D
from objectv3 import Objectv3
import tick
import threading
class Triangle(Objectv3):
    def __init__(self, v1: vector3.Vector3 , v2: vector3.Vector3 = None, v3: vector3.Vector3 = None, axes = None, **kwargs ) -> None:
        super().__init__( axes = axes)
        self.show_vertex_name = False 
        self.show_lengths = False 
        self.show_normal= False
        self.show_vertex_node = False 
        self.show_lines = False
        self.is_tessellate = False if 'is_tessellate' not in kwargs  else kwargs['is_tessellate']
        self.rng =  np.random.Generator(np.random.PCG64(42)) if 'rng' not in kwargs else kwargs['rng']
        # self.tesslte = triangle_stuff.tessellate.Tessellates

        self.v1 = v1
        self.v2 = v2
        self.v3 = v3

        self.pts[0] = v1
        self.pts[1] = v2
        self.pts[2] = v3
        self.pts = self.pts[:3] # triangle required 3 vertices
        self.center = ((self.pts[1] + self.pts[0] + self.pts[2])/3.0)
        self.bbox.update_box(self.pts, axes)
        self.bbox.remove_box()
        # set_tri_vertices(self)
        v1 = self.pts[0] .to_numpy() 
        v2 = self.pts[1] .to_numpy() 
        v3 = self.pts[2] .to_numpy() 
        self.e21 = v2 - v1
        self.e12 = v1 - v2

        self.l1 = np.linalg.norm(self.e21)
        self.e32 = v3 - v2
        self.e23 = v2 - v3

        self.l2 = np.linalg.norm(self.e32)
        self.e13 = v1 - v3
        self.e31 = v3 - v1

        self.l3 = np.linalg.norm(self.e13)
        self.l_largest = np
        assert(np.linalg.norm(np.cross(self.e32, self.e21) ) ) # e21 x e32 
        assert(np.linalg.norm(np.cross(self.e32, self.e13) ) ) # e13 x e32
        assert(np.linalg.norm(np.cross(self.e21, self.e13) ) ) # e13 x e21 

        cos_theta_1 = ((np.square(self.l2) + np.square(self.l3))  - np.square(self.l1) ) / (2 * self.l2 * self.l3 ) # angle eating line e32
        self.theta_1 = np.acos(cos_theta_1)
        cos_theta_2 = ((np.square(self.l1) + np.square(self.l3))  - np.square(self.l2) ) / (2 * self.l1 * self.l3 ) # angle eating line e13
        self.theta_2 = np.acos(cos_theta_2)
        cos_theta_3 = ((np.square(self.l1) + np.square(self.l2))  - np.square(self.l3) ) / (2 * self.l1 * self.l2 ) # angle eating line e21
        self.theta_3 = np.acos(cos_theta_3)
        self.triangle_type = classify (self.theta_1, self.theta_2, self.theta_3)
        self.perimeter = self.l1 + self.l2 + self.l3
        e21xe32 = np.cross(self.e32 , self.e21)
        self.area =  np.linalg.norm(e21xe32) / 2
        v4 = self.e32 + v1 # final vectices to create parralelogram 
        self.v4 = vector3.Vector3(*v4)
        self.e43 = v4 - v3 
        self.n = e21xe32# e21 x e32 (np.cross uses RHS so swap inputs)
        self.n_norm = self.n / np.linalg.norm(self.n)# e21 x e32 (np.cross uses RHS so swap inputs)
        
        self.plot_data = [ [Line3DCollection for _ in range(1)] , [Path3DCollection for _ in range(4)] , [Text3D for _ in range(4)] ,[Text3D for _ in range(3)] , [ [Line3D] for _ in range(5)]]
        self.incenter =   (self.v1*self.l1 + self.v2*self.l2 + self.v3*self.l3) / self.perimeter
        self.incenter_barycentric_coord = np.array([self.l1, self.l2, self.l3]) / self.perimeter
        self.incenter_inscribe_circle_radius = self.area / self.perimeter

        # do things 
        if self.is_tessellate:
            self.show(axes, 'lines')
            self.show(axes, 'vertex_node')

        else:
            self.show(axes, 'lines')
            self.show(axes, 'vertex_node')
            self.update_line()
            # self.show(axes, 'normal')
    def vertices(self):
        return self.v1, self.v2, self.v3
    def highlight(self, seconds = 1.0):
        lines = list(map( lambda x: x[0],  self.plot_data[4]))
        prev_lines_info = list(map(lambda ele: [ele.get_color(), ele.get_alpha()] ,    lines ))
        # print(prev_lines_info)
        self.update_line(color='green', alpha=1)
        
        if isinstance(seconds,float ):
            # print('lol')
            plt.pause(seconds)
            time.sleep(seconds)
            self.update_line(color=prev_lines_info[0][0] , alpha=prev_lines_info[0][1] )

    def get_lines(self):
        return self.plot_data[4]
        
    def update_line(self,**kwargs):
         for lines in self.plot_data[4]:
             for line in lines:
                if 'color' in kwargs:
                    line.set_color(kwargs['color']) 
                if 'alpha' in kwargs:
                    line.set_alpha(kwargs['alpha']) 

    def show(self, ax, mode = 'lines'):

        if mode == 'all' or mode == 'normal':
            if not self.show_normal:
                self.plot_data[0][:]  = [ax.quiver(*self.center.to_numpy(), *self.n,  linewidth=0.5, arrow_length_ratio=0.061)]
                self.show_normal = not self.show_normal

        if mode == 'all' or mode == 'vertex_node':
            if not self.show_vertex_node:
                self.plot_data[1][:] = [ 
                ax.scatter(*(self.v1.to_numpy()), s=0.6, color='pink'),
                ax.scatter(*(self.v2.to_numpy()), s=0.6, color='pink'),
                ax.scatter(*(self.v3.to_numpy()), s=0.6, color='pink'),
                # ax.scatter(*(self.v4.to_numpy()), s=0.4, color='black')
                ]
                self.show_vertex_node = not self.show_vertex_node

        if mode == 'all' or mode == 'vertex_name':
            if not self.show_vertex_name:
                self.plot_data[2][:] = [
                ax.text(*self.v1.to_numpy(), 'v1', fontsize=5), 
                ax.text(*self.v2.to_numpy(), 'v2', fontsize=5), 
                ax.text(*self.v3.to_numpy(), 'v3', fontsize=5), 
                # ax.text(*self.v4.to_numpy(), 'v4', fontsize=5), 
      
            ]
                self.show_vertex_name = not self.show_vertex_name

        if mode == 'all' or mode == 'lengths':
            if not self.show_lengths:
                self.plot_data[3][:] = [
                ax.text(* np.divide(self.v1.to_numpy()+self.v2.to_numpy(), 2), f'e21={np.linalg.norm(self.e21, ord=2):.3f}', fontsize=3 ), 
                ax.text(* np.divide(self.v3.to_numpy()+self.v2.to_numpy(), 2), f'e32={np.linalg.norm(self.e32, ord=2):.3f}', fontsize=3 ), 
                ax.text(* np.divide(self.v1.to_numpy()+self.v3.to_numpy(), 2), f'e13={np.linalg.norm(self.e13, ord=2):.3f}', fontsize=3 ), 
            ]
                self.show_lengths =  not self.show_lengths
        
        if mode == 'all' or  mode == 'lines':
            if not self.show_lines:
                self.plot_data[4][:] = [
                    ax.plot(*zip(self.v1.to_numpy(),self.v2.to_numpy()), color='blue', linewidth=0.5, alpha=0.7) ,
                    ax.plot(*zip(self.v2.to_numpy(),self.v3.to_numpy()), color='blue', linewidth=0.5, alpha=0.7) ,
                    ax.plot(*zip(self.v1.to_numpy(),self.v3.to_numpy()), color='blue', linewidth=0.5, alpha=0.7) , 
                    # ax.plot(*zip(self.v1.to_numpy(),self.v4.to_numpy()), linewidth=0.5, alpha=0.2, linestyle='--', color='blue'),
                    # ax.plot(*zip(self.v4.to_numpy(),self.v3.to_numpy()), linewidth=0.5, alpha=0.2 , linestyle='--', color='blue')
                ]
                self.show_lines = not self.show_lines

    def unshow(self, mode='all'):
        if mode == 'all':
            self.unshow('normal')
            self.unshow('vertex_node')
            self.unshow('vertex_name')
            self.unshow('lengths')
            self.unshow('lines')

        elif mode == 'normal':
            if self.show_normal:
                for ele in self.plot_data[0]:
                    ele.remove() 
            self.show_normal = False
        elif mode == 'vertex_node':
            if self.show_vertex_node:
                for ele in self.plot_data[1]:
                    ele.remove() 
            self.show_vertex_node = False
        elif mode == 'vertex_name':
            if self.show_vertex_name:
                for ele in self.plot_data[2]:
                    ele.remove() 
            self.show_vertex_name = False
        elif mode == 'lengths':
            if self.show_lengths:
                for ele in self.plot_data[3]:
                    ele.remove() 
            self.show_lengths = False
        elif mode == 'lines':
            if self.show_lines:
                for lines in  self.plot_data[4]:
                    for line in lines:
                        line.remove()
            self.show_lines = False
    
    # hidden method
    def add_collection(self, **kwargs):
        pass
    
    # hidden method
    def load_mesh(self, **kwargs):
        pass
    
    def barycentric_to_coord(self, b1, b2, b3) -> vector3.Vector3:
        if (b1 + b2 + b3) - 1 > 0.09:
            raise ValueError('barycentric coordinates sum must equal 1')
        return self.v1 * b1 + self.v2 * b2 + self.v3 * b3
        
    def coord_to_barycentric(self, pt: vector3.Vector3):
        u1 = 0.0; u2= 0.0; u3 = 0.0; u4 = 0.0 
        v1 = 0.0; v2= 0.0; v3 = 0.0; v4 = 0.0
        normal = vector3.Vector3(*self.n)
        if (np.abs(normal.x) > np.abs(normal.y))  and ( np.abs(normal.x) > np.abs(normal.z)):
            # discard x , yz plane projection
            u1 = self.v1.y - self.v3.y
            u2 = self.v2.y - self.v3.y
            u3 = pt.y - self.v1.y
            u4 = pt.y - self.v3.y
            v1 = self.v1.z - self.v3.z
            v2 = self.v2.z - self.v3.z
            v3 = pt.z - self.v1.z
            v4 = pt.z - self.v3.z
        elif np.abs(normal.y) > np.abs(normal.z):
            # discard y , xz projection 
            u1 = self.v1.z - self.v3.z
            u2 = self.v2.z - self.v3.z
            u3 = pt.z - self.v1.z
            u4 = pt.z - self.v3.z
            v1 = self.v1.x - self.v3.x
            v2 = self.v2.x - self.v3.x
            v3 = pt.x - self.v1.x
            v4 = pt.x - self.v3.x
        else:
            # discard z , xy projection 
            u1 = self.v1.x - self.v3.x
            u2 = self.v2.x - self.v3.x
            u3 = pt.x - self.v1.x
            u4 = pt.x - self.v3.x
            v1 = self.v1.y - self.v3.y
            v2 = self.v2.y - self.v3.y
            v3 = pt.y - self.v1.y
            v4 = pt.y - self.v3.y

        denom = v1 *u2 - v2*u1
        if denom == 0:
            return False # bogus triangle (i.e. zero area)
        one_over_denom = 1.0/ denom
        b0 = (v4*u2 - v2*u4) * one_over_denom
        b1 = (v1*u3 - v3*u1) * one_over_denom
        b2 = 1 - b0 - b1
        return np.array([b0, b1, b2])
        # n_norm = self.n / np.linalg.norm(self.n, ord=2)
        # d1 = pt.to_numpy() - self.v1.to_numpy()
        # d2 = pt.to_numpy() - self.v2.to_numpy()
        # d3 = pt.to_numpy() - self.v3.to_numpy()
        # area = np.dot(np.cross (self.e13, self.e32), n_norm) /2.0  # self.e32 x self.e13
        # area_1 = np.dot(np.cross (d3, self.e32), n_norm) /2.0 # self.e32 x d3
        # area_2 = np.dot(np.cross (d1, self.e13), n_norm) /2.0 # self.e13 x d1
        # area_3 = np.dot(np.cross (d2, self.e21), n_norm)/2.0 # self.e21 x d2
        # b1 = area_1 / area
        # b2 = area_2 / area
        # b3 = area_3 / area
        # return np.array([b1, b2, b3])
    ###
    def tessellate(self):
        searchable_nets_per_parent = self.pts.size - 1 if (self.pts.size - 1 ) < 6 else 6 
        lock = threading.Lock()
        # self.tesslte = triangle_stuff.tessellate.Tessellates(mode='load', num_nodes =self.pts.size , axes=self.axes,  is_tessellate=True)
        # threads = [ 
        # threading.Thread( target=thr_triangle,  args=( self.pts[i], self.pts, list(range(0, i)) + list(range(i + 1, self.pts.size)),  [[np.finfo(np.float64).max, vector3.Vector3] for _ in range(searchable_nets_per_parent)]  ,searchable_nets_per_parent,  self.tesslte , self.axes, lock) )  # map
        #     for i in range(self.pts.size)
        # ]
        # for thr in threads:
        #     thr.start()
        # for thr in threads:
        #     thr.join()
        # self.tesslte.sweep()




def barycentric_to_coord(parent, b1, b2, b3) -> vector3.Vector3:
        if (b1 + b2 + b3) - 1 > 0.001:
            return vector3.Vector3()
            # raise ValueError('barycentric coordinates sum must equal 1')
        return parent.v1 * b1 + parent.v2 * b2 + parent.v3 * b3

def coord_to_barycentric(parent, pt: vector3.Vector3,):
    u1 = 0.0; u2= 0.0; u3 = 0.0; u4 = 0.0 
    v1 = 0.0; v2= 0.0; v3 = 0.0; v4 = 0.0
    normal = vector3.Vector3(*parent.n)
    if (np.abs(normal.x) > np.abs(normal.y))  and ( np.abs(normal.x) > np.abs(normal.z)):
        # discard x , yz plane projection
        u1 = parent.v1.y - parent.v3.y
        u2 = parent.v2.y - parent.v3.y
        u3 = pt.y - parent.v1.y
        u4 = pt.y - parent.v3.y
        v1 = parent.v1.z - parent.v3.z
        v2 = parent.v2.z - parent.v3.z
        v3 = pt.z - parent.v1.z
        v4 = pt.z - parent.v3.z
    elif np.abs(normal.y) > np.abs(normal.z):
        # discard y , xz projection 
        u1 = parent.v1.z - parent.v3.z
        u2 = parent.v2.z - parent.v3.z
        u3 = pt.z - parent.v1.z
        u4 = pt.z - parent.v3.z
        v1 = parent.v1.x - parent.v3.x
        v2 = parent.v2.x - parent.v3.x
        v3 = pt.x - parent.v1.x
        v4 = pt.x - parent.v3.x
    else:
        # discard z , xy projection 
        u1 = parent.v1.x - parent.v3.x
        u2 = parent.v2.x - parent.v3.x
        u3 = pt.x - parent.v1.x
        u4 = pt.x - parent.v3.x
        v1 = parent.v1.y - parent.v3.y
        v2 = parent.v2.y - parent.v3.y
        v3 = pt.y - parent.v1.y
        v4 = pt.y - parent.v3.y

    denom = v1 *u2 - v2*u1
    if denom == 0:
        return False # bogus triangle (i.e. zero area)
    one_over_denom = 1.0/ denom
    b0 = (v4*u2 - v2*u4) * one_over_denom
    b1 = (v1*u3 - v3*u1) * one_over_denom
    b2 = 1 - b0 - b1
    return np.array([b0, b1, b2])
def barycentric_point(vertices:np.ndarray, b_coord: np.ndarray)-> np.ndarray:
    """calculate weights of three vectors
    

    Args:
        vectors - three 3D vectors of numpy type
        b_coord - three barycentric weights (b_0, b_1, b_2)
    
        
    Return:
        3D point
    """
    if (b_coord.size == 3 and vertices.size == 3):
        raise ValueError()
    return np.sum(b_coord[:, None] * vertices, axis=0)
    
def rand_barycentric():
    global ax
    """compute random set of barycentric"""
    if np.random.random() > 0.5:
        b0  = np.random.random()
        b1 = b2 = (1 - b0)/2
    else:
        b0  = -0.2 #np.random.normal(loc=0)
        b1  = 0.6 #np.random.normal(loc=0 )
        b2  = 0.6 # np.random.normal(loc=0)
    ax.set_title([b0,b1,b2])
    return np.array([b0, b1, b2])

def set_tri_vertices(self: Triangle):
    """create/set triangle vertices in LHS ruling"""
    boxx_diff = self.bbox.vmax - self.bbox.vmin
    pos_id = np.argmax(np.abs(boxx_diff.to_numpy()))

    if pos_id == 0: # x box-width is largest
                
        if self.pts[0].x == self.bbox.vmax.x:
            self.v1 = self.pts[0]
            if self.pts[1].z == self.bbox.vmax.z:
                self.v2 = self.pts[1]
                self.v3 = self.pts[2]
            else:
                self.v2 = self.pts[2]
                self.v3 = self.pts[1]
        elif self.pts[1].x == self.bbox.vmax.x:
            self.v1 = self.pts[1]
            if self.pts[0].z == self.bbox.vmax.z:
                self.v2 = self.pts[0]
                self.v3 = self.pts[2]
            else:
                self.v2 = self.pts[2]
                self.v3 = self.pts[0]
        elif self.pts[2].x == self.bbox.vmax.x:
            self.v1 = self.pts[2]
            if self.pts[0].z  == self.bbox.vmax.z:
                self.v2 = self.pts[0]
                self.v3 = self.pts[1]
            else:
                self.v2 = self.pts[1]
                self.v3 = self.pts[0]
    
    if pos_id == 1: # y box-width is largest
            
        if self.pts[0].y == self.bbox.vmax.y:
            self.v1 = self.pts[0]
            if self.pts[1].x == self.bbox.vmax.x:
                self.v2 = self.pts[1]
                self.v3 = self.pts[2]
            else :
                self.v2 = self.pts[2]
                self.v3 = self.pts[1]
        elif self.pts[1].y == self.bbox.vmax.y:
            self.v1 = self.pts[1]
            if self.pts[0].x == self.bbox.vmax.x:
                self.v2 = self.pts[0]
                self.v3 = self.pts[2]
            else :
                self.v2 = self.pts[2]
                self.v3 = self.pts[0]
        elif self.pts[2].y == self.bbox.vmax.y:
            self.v1 = self.pts[2]
            if self.pts[0].x == self.bbox.vmax.x:
                self.v2 = self.pts[0]
                self.v3 = self.pts[1]
            else:
                self.v2 = self.pts[1]
                self.v3 = self.pts[0]

    if pos_id == 2: # z box-width is largest
            
        if self.pts[0].z == self.bbox.vmax.z:
            self.v1 = self.pts[0] # pts[0] contributes to max bound on z-axis
            if self.pts[1].x == self.bbox.vmax.x:
                    self.v2 = self.pts[1] # pts[1] contributes to max bound on x-axis
                    self.v3 = self.pts[2] # pts[2] contributes to max bound on y-axis
            else:
                self.v2 = self.pts[1]
                self.v3 = self.pts[2]
        
        elif self.pts[1].z == self.bbox.vmax.z:
            self.v1 = self.pts[1]
            if self.pts[0].x == self.bbox.vmax.x:
                self.v2 = self.pts[0]
                self.v3 = self.pts[2]
            else:
                self.v2 = self.pts[2]
                self.v3 = self.pts[0]
        
        elif self.pts[2].z == self.bbox.vmax.z:
            self.v1 = self.pts[2]
            if self.pts[0].x == self.bbox.vmax.x:
                self.v2 = self.pts[0]
                self.v3 = self.pts[1]
            else:
                self.v2 = self.pts[1]
                self.v3 = self.pts[0]

def classify(*angles_rad):
    res = ''
    for radians in angles_rad:
        deg = np.rad2deg(radians)
        if deg == 90 and res.find('right') == -1:
            res += 'right '
        if deg > 90 and res.find('obtuse') == -1:
            res += 'obtuse'
    return 'acute' if len(res) == 0 else res

def isosceles_triangle(equal_side_len = 1, plane = 'xy' ):
    """generate vertices for right triangle on xy, yz, or xz plane"""
    if  equal_side_len <= 0:
        raise ValueError(f'equal_side_len must be greater than 0')
    base = equal_side_len / np.sqrt(2)
    v1,v2,v3, v4, = right_triangle(base, plane)
    v1 = -1*v3
    v4 =  v2 + (v3- v1)
    return v1,v2,v3, v4

def right_triangle(length = 1, plane='xy'):
    """generate vertices for right triangle on xy, yz, or xz plane"""
    if length <= 0:
        raise ValueError('function handles only positive lengths at the moment')
    if plane in ['xy', 'yx'] :
        v1 = vector3.Vector3(0, 0,0)
        v2 = vector3.Vector3(0, length, 0)
        v3 = vector3.Vector3(length, 0)
    elif plane in ['yz', 'zy']:
        v1 = vector3.Vector3(0, 0, 0)
        v3 = vector3.Vector3(0, length, 0)
        v2 = vector3.Vector3(0, 0, length)
    elif plane in ['xz', 'zx']:
        v1 = vector3.Vector3(0, 0, 0)
        v2 = vector3.Vector3(0,0,length)
        v3 = vector3.Vector3(length,0,0)
    else:
        raise ValueError('invalid plane')
    v4 =  v2 + (v3- v1)

    return v1, v2, v3, v4

def obtuse_triangle (theta_2: float, theta_3: float = 0.0, theta_1: float = 0.0, plane='xy'):
    width = 2 

    if not (theta_2 > 90 and theta_2 < 180):
        raise ValueError('obtuse triangle must be between 90 and 180')

    random_value = np.random.random()
    
    if random_value < 0.5:
        # titled obtuse triangle 
        angle_of_height = np.deg2rad(180 - theta_2)
        height_over_hypotenuse = np.sin(angle_of_height) 
        left_displacement_from_origin = height_over_hypotenuse / np.tan(angle_of_height)
        right_displacement_from_origin = 1
        if plane in  ['xy' , 'yx']: 
            v1 = vector3.Vector3()
            v2 = vector3.Vector3( - left_displacement_from_origin, height_over_hypotenuse, 0)
            v3 = vector3.Vector3( right_displacement_from_origin, 0 , 0)
        elif plane in  ['yz' , 'zy']: 
            v1 = vector3.Vector3()
            v2 = vector3.Vector3( 0,- left_displacement_from_origin, height_over_hypotenuse)
            v3 = vector3.Vector3( 0, right_displacement_from_origin , 0)
        elif plane in ['xz' , 'zx']: 
            v1 = vector3.Vector3()
            v2 = vector3.Vector3( - left_displacement_from_origin, 0, height_over_hypotenuse)
            v3 = vector3.Vector3( right_displacement_from_origin, 0 , 0)
        else:
            raise ValueError()
    else:
        # flat base obtuse triangle 
        if np.abs( (theta_2 + theta_3) - (180 - theta_2) )  > 0.001: 
            theta_1 = theta_3 = (180 - theta_2) * 0.5
        theta_3_rad = np.deg2rad(theta_3)
        theta_2_rad = np.deg2rad(theta_2)
        theta_1_rad = np.deg2rad( theta_1)
        if plane in  ['xy' , 'yx']: 
            v1 =  vector3.Vector3(  -np.sin(theta_1_rad) / np.tan(theta_1_rad), 0, 0)
            v2 =  vector3.Vector3(0,np.sin(theta_3_rad),0)
            v3 =  vector3.Vector3(np.sin(theta_3_rad) / np.tan(theta_3_rad), 0, 0)
            v4 =  v2 + (v3- v1)
        elif plane in  ['yz' , 'zy']: 
            v1 =  vector3.Vector3( 0, -np.sin(theta_1_rad) / np.tan(theta_1_rad), 0)
            v2 =  vector3.Vector3(0,0,np.sin(theta_3_rad))
            v3 =  vector3.Vector3(0,np.sin(theta_3_rad) / np.tan(theta_3_rad), 0)
        elif plane in  ['xz' , 'zx']: 
            v1 =  vector3.Vector3( -np.sin(theta_1_rad) / np.tan(theta_1_rad),0, 0)
            v2 =  vector3.Vector3(0, 0, np.sin(theta_3_rad))
            v3 =  vector3.Vector3(np.sin(theta_3_rad) / np.tan(theta_3_rad), 0, 0)
        else:
            raise ValueError()
    v4 =  v2 + (v3- v1)
        
    return (v1, v2, v3, v4)

if __name__ == '__main__':
    fig = plt.figure() 

    ax11 = fig.add_subplot(3, 3, 1, projection='3d')
    ax12 = fig.add_subplot(3, 3, 2, projection='3d')
    ax13 = fig.add_subplot(3, 3, 3, projection='3d')
    ax11.set_xticks([], []); ax11.set_yticks([], []); ax11.set_zticks
    ax12.set_xticks([], []); ax12.set_yticks([], []); ax12.set_zticks
    ax13.set_xticks([], []); ax13.set_yticks([], []); ax13.set_zticks
    v1,v2,v3,v4 = obtuse_triangle(theta_2= 135, plane='xy' )
    ax11.plot(*zip(v1.to_numpy(), v2.to_numpy()), linewidth = 0.5, c='red' , alpha=0.6)
    ax11.plot(*zip(v2.to_numpy(), v3.to_numpy()), linewidth = 0.5, c='red' , alpha=0.6)
    ax11.plot(*zip(v3.to_numpy(), v1.to_numpy()), linewidth = 0.5, c='red' , alpha=0.6)
    ax11.plot(*zip(v2.to_numpy(), v4.to_numpy()), linewidth = 0.5, c='silver' , alpha=0.6)
    ax11.plot(*zip(v4.to_numpy(), v3.to_numpy()), linewidth = 0.5, c='silver' , alpha=0.6)
    ax11.text(*v1.to_numpy(), 'v1', fontsize=3), 
    ax11.text(*v2.to_numpy(), 'v2', fontsize=3), 
    ax11.text(*v3.to_numpy(), 'v3', fontsize=3), 
    ax11.text(*v4.to_numpy(), 'v4', fontsize=3), 
    v1,v2,v3,v4 = obtuse_triangle(theta_2= 135, plane='yz' )
    ax12.plot(*zip(v1.to_numpy(), v2.to_numpy()), linewidth = 0.5, c='red' , alpha=0.6)
    ax12.plot(*zip(v2.to_numpy(), v3.to_numpy()), linewidth = 0.5, c='red' , alpha=0.6)
    ax12.plot(*zip(v3.to_numpy(), v1.to_numpy()), linewidth = 0.5, c='red' , alpha=0.6)
    ax12.plot(*zip(v2.to_numpy(), v4.to_numpy()), linewidth = 0.5, c='silver' , alpha=0.6)
    ax12.plot(*zip(v4.to_numpy(), v3.to_numpy()), linewidth = 0.5, c='silver' , alpha=0.6)
    ax12.text(*v1.to_numpy(), 'v1', fontsize=3), 
    ax12.text(*v2.to_numpy(), 'v2', fontsize=3), 
    ax12.text(*v3.to_numpy(), 'v3', fontsize=3), 
    ax12.text(*v4.to_numpy(), 'v4', fontsize=3), 
    v1,v2,v3,v4 = obtuse_triangle(theta_2= 135, plane='xz' )
    ax13.plot(*zip(v1.to_numpy(), v2.to_numpy()), linewidth = 0.5, c='red' , alpha=0.6)
    ax13.plot(*zip(v2.to_numpy(), v3.to_numpy()), linewidth = 0.5, c='red' , alpha=0.6)
    ax13.plot(*zip(v3.to_numpy(), v1.to_numpy()), linewidth = 0.5, c='red' , alpha=0.6)
    ax13.plot(*zip(v2.to_numpy(), v4.to_numpy()), linewidth = 0.5, c='silver' , alpha=0.6)
    ax13.plot(*zip(v4.to_numpy(), v3.to_numpy()), linewidth = 0.5, c='silver' , alpha=0.6)
    ax13.text(*v1.to_numpy(), 'v1', fontsize=3), 
    ax13.text(*v2.to_numpy(), 'v2', fontsize=3), 
    ax13.text(*v3.to_numpy(), 'v3', fontsize=3), 
    ax13.text(*v4.to_numpy(), 'v4', fontsize=3), 

    ax21 = fig.add_subplot(3, 3, 4, projection='3d')
    ax22 = fig.add_subplot(3, 3, 5, projection='3d')
    ax23 = fig.add_subplot(3, 3, 6, projection='3d')
    ax21.set_xticks([], []); ax21.set_yticks([], []); ax21.set_zticks
    ax22.set_xticks([], []); ax22.set_yticks([], []); ax22.set_zticks
    ax23.set_xticks([], []); ax23.set_yticks([], []); ax23.set_zticks
    
    v1,v2,v3,v4 = isosceles_triangle( plane='xy' )
    ax21.plot(*zip(v1.to_numpy(), v2.to_numpy()), linewidth = 0.5, c='red' , alpha=0.6)
    ax21.plot(*zip(v2.to_numpy(), v3.to_numpy()), linewidth = 0.5, c='red' , alpha=0.6)
    ax21.plot(*zip(v3.to_numpy(), v1.to_numpy()), linewidth = 0.5, c='red' , alpha=0.6)
    ax21.plot(*zip(v2.to_numpy(), v4.to_numpy()), linewidth = 0.5, c='silver' , alpha=0.6)
    ax21.plot(*zip(v4.to_numpy(), v3.to_numpy()), linewidth = 0.5, c='silver' , alpha=0.6)
    ax21.text(*v1.to_numpy(), 'v1', fontsize=3), 
    ax21.text(*v2.to_numpy(), 'v2', fontsize=3), 
    ax21.text(*v3.to_numpy(), 'v3', fontsize=3), 
    ax21.text(*v4.to_numpy(), 'v4', fontsize=3), 
    v1,v2,v3, v4 = isosceles_triangle( plane='yz' )
    ax22.plot(*zip(v1.to_numpy(), v2.to_numpy()), linewidth = 0.5, c='red' , alpha=0.6)
    ax22.plot(*zip(v2.to_numpy(), v3.to_numpy()), linewidth = 0.5, c='red' , alpha=0.6)
    ax22.plot(*zip(v3.to_numpy(), v1.to_numpy()), linewidth = 0.5, c='red' , alpha=0.6)
    ax22.plot(*zip(v2.to_numpy(), v4.to_numpy()), linewidth = 0.5, c='silver' , alpha=0.6)
    ax22.plot(*zip(v4.to_numpy(), v3.to_numpy()), linewidth = 0.5, c='silver' , alpha=0.6)
    ax22.text(*v1.to_numpy(), 'v1', fontsize=3), 
    ax22.text(*v2.to_numpy(), 'v2', fontsize=3), 
    ax22.text(*v3.to_numpy(), 'v3', fontsize=3), 
    ax22.text(*v4.to_numpy(), 'v4', fontsize=3), 
    v1,v2,v3, v4 = isosceles_triangle( plane='xz' )
    ax23.plot(*zip(v1.to_numpy(), v2.to_numpy()), linewidth = 0.5, c='red' , alpha=0.6)
    ax23.plot(*zip(v2.to_numpy(), v3.to_numpy()), linewidth = 0.5, c='red' , alpha=0.6)
    ax23.plot(*zip(v3.to_numpy(), v1.to_numpy()), linewidth = 0.5, c='red' , alpha=0.6)
    ax23.plot(*zip(v2.to_numpy(), v4.to_numpy()), linewidth = 0.5, c='silver' , alpha=0.6)
    ax23.plot(*zip(v4.to_numpy(), v3.to_numpy()), linewidth = 0.5, c='silver' , alpha=0.6)
    ax23.text(*v1.to_numpy(), 'v1', fontsize=3), 
    ax23.text(*v2.to_numpy(), 'v2', fontsize=3), 
    ax23.text(*v3.to_numpy(), 'v3', fontsize=3), 
    ax23.text(*v4.to_numpy(), 'v4', fontsize=3), 

    ax31 = fig.add_subplot(3, 3, 7, projection='3d')
    ax32 = fig.add_subplot(3, 3, 8, projection='3d')
    ax33 = fig.add_subplot(3, 3, 9, projection='3d')
    ax31.set_xticks([], []); ax31.set_yticks([], []); ax31.set_zticks
    ax32.set_xticks([], []); ax32.set_yticks([], []); ax32.set_zticks
    ax33.set_xticks([], []); ax33.set_yticks([], []); ax33.set_zticks
    v1,v2,v3, v4  = right_triangle( plane='xy' )
    ax31.plot(*zip(v1.to_numpy(), v2.to_numpy()), linewidth = 0.5, c='red' , alpha=0.6)
    ax31.plot(*zip(v2.to_numpy(), v3.to_numpy()), linewidth = 0.5, c='red' , alpha=0.6)
    ax31.plot(*zip(v3.to_numpy(), v1.to_numpy()), linewidth = 0.5, c='red' , alpha=0.6)
    ax31.plot(*zip(v2.to_numpy(), v4.to_numpy()), linewidth = 0.5, c='silver' , alpha=0.6)
    ax31.plot(*zip(v4.to_numpy(), v3.to_numpy()), linewidth = 0.5, c='silver' , alpha=0.6)
    ax31.text(*v1.to_numpy(), 'v1', fontsize=3), 
    ax31.text(*v2.to_numpy(), 'v2', fontsize=3), 
    ax31.text(*v3.to_numpy(), 'v3', fontsize=3), 
    ax31.text(*v4.to_numpy(), 'v4', fontsize=3), 
    v1,v2,v3,v4  = right_triangle( plane='yz' )
    ax32.plot(*zip(v1.to_numpy(), v2.to_numpy()), linewidth = 0.5, c='red' , alpha=0.6)
    ax32.plot(*zip(v2.to_numpy(), v3.to_numpy()), linewidth = 0.5, c='red' , alpha=0.6)
    ax32.plot(*zip(v3.to_numpy(), v1.to_numpy()), linewidth = 0.5, c='red' , alpha=0.6)
    ax32.plot(*zip(v2.to_numpy(), v4.to_numpy()), linewidth = 0.5, c='silver' , alpha=0.6)
    ax32.plot(*zip(v4.to_numpy(), v3.to_numpy()), linewidth = 0.5, c='silver' , alpha=0.6)
    ax32.text(*v1.to_numpy(), 'v1', fontsize=3), 
    ax32.text(*v2.to_numpy(), 'v2', fontsize=3), 
    ax32.text(*v3.to_numpy(), 'v3', fontsize=3), 
    ax32.text(*v4.to_numpy(), 'v4', fontsize=3), 

    v1,v2,v3,v4 = right_triangle( plane='xz' )
    ax33.plot(*zip(v1.to_numpy(), v2.to_numpy()), linewidth = 0.5, c='red' , alpha=0.6)
    ax33.plot(*zip(v2.to_numpy(), v3.to_numpy()), linewidth = 0.5, c='red' , alpha=0.6)
    ax33.plot(*zip(v3.to_numpy(), v1.to_numpy()), linewidth = 0.5, c='red' , alpha=0.6)
    ax33.plot(*zip(v2.to_numpy(), v4.to_numpy()), linewidth = 0.5, c='silver' , alpha=0.6)
    ax33.plot(*zip(v4.to_numpy(), v3.to_numpy()), linewidth = 0.5, c='silver' , alpha=0.6)
    ax33.text(*v1.to_numpy(), 'v1', fontsize=3), 
    ax33.text(*v2.to_numpy(), 'v2', fontsize=3), 
    ax33.text(*v3.to_numpy(), 'v3', fontsize=3), 
    ax33.text(*v4.to_numpy(), 'v4', fontsize=3), 

    plt.show()

