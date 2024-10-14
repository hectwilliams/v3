import objectv3
import numpy as np
import vector3
import matplotlib.pyplot as plt
from  mpl_toolkits.mplot3d.art3d import Line3D
import trianglenode
import tick

class Polygon(objectv3.Objectv3):
    def __init__(self, num_sides, center, axes, radius=1.0, theta_offset=0.0, kx= 1.0, ky=1.0, xy_is_mesh_grid=False, mesh_mode = 0, subclass_name = None):
        super().__init__(center, axes)
        self.poly_num_sides = num_sides
        self.radius = radius
        self.center = center 
        self.subclass_name = subclass_name
        if num_sides <= 2:
            raise ValueError('polygons requires at least 4 sides ')
        theta = np.deg2rad(np.linspace(theta_offset , 360, num=num_sides + 1))[:num_sides]
        self.poly_num_sides = num_sides
        self.mesh_mode = 0
        self.cur_mode_mode = 0
        self.prev_mode_mode = None
        self.num_supported_mesh = 2
        self.xy_is_mesh_grid = xy_is_mesh_grid
        alpha = ((np.pi/2) -  theta)
        x = kx * radius * np.cos(alpha)
        self.x = x 
        y = ky * radius * np.sin(alpha)
        self.y = y 
        z = np.zeros(shape=x.shape)
        self.z = z

        """loads datapoints and creates triangulation"""
        if not self.xy_is_mesh_grid:
            self.load_mesh(self.x, self.y ,self.z) # change method new TODO 
            self.triangulate_mesh_contour( self.mesh_mode)
        if self.xy_is_mesh_grid:
            self.load_mesh(*generator_grid(self.subclass_name, self.x , self.y, self.radius)) 
            self.triangulate_mesh_grid()
        self.mesh = mesh(self)


    def show_mesh_plot(self, **kwargs):
        """Draw simple mesh
        
        Methods with _plot suffix follow matplotlib's axes.plot.kwargs dictionary structure
        """
        if hasattr(self, 'mesh'):
            for node in self.mesh:
                node.plot_node(**kwargs)
    def renove_mesh_plot(self):
        """Remove triangle mesh on polygon"""
        if hasattr(self, 'mesh'):
            for node in self.mesh:
                node.remove_node()
    def toggle_mesh(self, ):
        
        if hasattr(self, 'aninmation_on'):
            print('hector willidms')

        if hasattr(self, 'mesh'):
            if self.xy_is_mesh_grid:
                for node in self.mesh:
                    node.toggle_node()
            else:
                if  self.cur_mode_mode   == self.num_supported_mesh:
                    self.cur_mode_mode = 0
                    for node in self.mesh:
                        node.toggle_node()
                else:
                    self.renove_mesh_plot()
                    self.triangulate_mesh_contour(self.cur_mode_mode)
                    self.mesh = mesh(self)
                    self.show_mesh_plot(c = 'black')
                    self.prev_mode_mode = self.cur_mode_mode
                    self.cur_mode_mode = (self.cur_mode_mode + 1) 
                    
    def show_triangulation_normal(self):
        """show triangle normals"""
        if hasattr(self, 'mesh'):
            for node in self.mesh:
                node.plot_normal()
    def remove_triangulation_normal(self):
        """remove triangle normal"""
        if hasattr(self, 'mesh'):
            for node in self.mesh:
                node.remove_normal()
    def re_sequencer(self):
        """reload local buffers; function must be called after polygon points been updated"""
        data = np.array(list(map(lambda ele: ele.to_numpy(), self.pts)))
        self.x = data[:, 0]
        self.y = data[:, 1]
        self.z = data[:, 2]
        if not self.xy_is_mesh_grid:
            self.triangulate_mesh_contour( self.mesh_mode)
        else:
            self.triangulate_mesh_grid()
        self.mesh = mesh(self)
    def xform(self, m):
        self.renove_mesh_plot()
        self.disconnect_vertices()
        super().xform(m)
        self.re_sequencer()
    def xform_q(self, q):
        super().xform_q(q)
        self.re_sequencer()
    def triangulate_mesh_contour(self, mode = 0):
        """ fanning style mesh """
        if mode == 0:
            self.triangle_list = np.array([  [vector3.Vector3, vector3.Vector3,  vector3.Vector3] for _ in range( self.poly_num_sides-2)])
            for i in range(self.poly_num_sides -2):
                i_plus_1 = i + 1
                i_plus_2 = i + 2
                self.triangle_list[i][0] =  vector3.Vector3(self.x[0],        self.y[0] ,        self.z[0])
                self.triangle_list[i][1] =  vector3.Vector3(self.x[i_plus_1], self.y[i_plus_1] , self.z[i_plus_1])
                self.triangle_list[i][2]  = vector3.Vector3(self.x[i_plus_2], self.y[i_plus_2] , self.z[i_plus_2])
        elif mode == 1:
            """ pizza syle mesh """
            self.triangle_list = np.array([  [vector3.Vector3, vector3.Vector3,  vector3.Vector3] for _ in range(self.poly_num_sides + 2)])
            prev = -3
            next = -2
            for i in range(self.poly_num_sides + 2  ):
                self.triangle_list[i][0] =  self.center
                self.triangle_list[i][1] =  vector3.Vector3(self.x[prev], self.y[prev] , self.z[prev])
                self.triangle_list[i][2]  = vector3.Vector3(self.x[next], self.y[next] , self.z[next])
                prev = next 
                next = next + 1
        else :
            raise ValueError("invalid mode")
    
    def triangulate_mesh_grid(self):
        a_curr = self.pts[0]
        select_tick = 0
        a_prev = None
        self.triangle_list = np.array([  [vector3.Vector3, vector3.Vector3,  vector3.Vector3] for _ in range( int(self.pts.size * 1.5) )])
        self.index = tick.Tick()
        pts_size_over_2  = self.pts.size//2
        
        for pts in [  self.pts[0:pts_size_over_2], self.pts[pts_size_over_2:] ]:
            last_point = None 
            arr = [[], []]
            for pt in pts:
                a_prev = a_curr
                a_curr = pt
                arr[select_tick].append(a_curr)
                if a_curr.x != a_prev.x:
                    select_tick += 1
                    if select_tick == 2:

                        self.process_arrs(*arr)
                        select_tick = 1
                        arr[0] = arr[1] + []
                        arr[1] = []
                self.axes.view_init(29, -3, 0)
                last_point = pt 
            self.process_arrs([last_point],arr[0])
        self.triangle_list = self.triangle_list[: self.index.value ]
        del self.index


    def process_arrs (self, a_list, b_list ) :
        if not a_list or not b_list:
            return 
        a = a_list
        b = b_list
        if a_list.__len__() < b_list.__len__():
            b = a_list
            a = b_list
        # sort about y axis (increasing)
        a = sorted(a, key=lambda v: v.y)
        b = sorted(b, key=lambda v: v.y)
        a_next = 0
        b_next = 0
        a_prev = 0
        b_prev = 0 
        stride = int(np.floor (len(a) / len(b)))
        while  a_next + stride < len(a):
            a_prev = a_next
            a_next =  a_next + stride
            self.triangle_list[self.index.tick()][0:3] =  a[a_prev] , a[a_next], b[b_next] 
            if b_next + stride < len(b):
                b_prev = b_next
                b_next = b_next + stride 
            else:
                b_next = len(b) - 1
        if len(b) == 1:
            for i in range(len(a) - 1):
                self.triangle_list[self.index.tick()][0:3] =  a[i] , a[i + 1], b[b_next] 
        else:        
            self.triangle_list[self.index.tick()][0:3] =  a[a_next] , a[a_prev], b[b_next] 
            
    def draw_triangle(self, v1,v2,v3, axes):
            axes.plot(*zip(v1.to_numpy(), v2.to_numpy()) , linewidth=0.5, c='blue')
            axes.plot(*zip(v2.to_numpy(), v3.to_numpy()), linewidth=0.5, c='blue')
            axes.plot(*zip(v3.to_numpy(), v1.to_numpy()), linewidth=0.5, c='blue')

def mesh(polygon: Polygon)->np.ndarray:
    if hasattr(polygon, 'triangle_list'):
        return np.array( [ trianglenode.Trianglenode(polygon.triangle_list[i][0], polygon.triangle_list[i][1], polygon.triangle_list[i][2]  , polygon.axes) for i in range ( len(polygon.triangle_list)  )  ] )
    
def generator_grid(name: str, x: np.ndarray, y: np.ndarray, radius =1,  is_flat = False) :
    if name == 'Circle':
        xx, yy = np.meshgrid(x, y)
        xx = xx.flatten() 
        yy = yy.flatten() 
        u = np.square(radius) - (np.square(xx) + np.square(yy) ) 
        negative_incides = np.nonzero( u < 0)
        xx = np.delete(xx, negative_incides)
        yy = np.delete(yy, negative_incides)
        zz =  np.sqrt(radius **2.0 - (xx**2.0 + yy**2.0) ) if not is_flat else np.zeros(shape=xx.shape)
        
        xx = xx.round(5)
        yy = yy.round(5)
        zz = zz.round(5)

        stacked_arrays = np.column_stack( ( xx, yy, zz) )
        _, indices = np.unique(stacked_arrays, return_index=True, axis=0)
        stacked_unique = stacked_arrays[indices]
        x = np.hstack( ( stacked_unique[:, 0 ] , stacked_unique[:, 0] ))
        y = np.hstack( ( stacked_unique[:, 1 ] , stacked_unique[:, 1] ))
        z = np.hstack( ( stacked_unique[:, 2 ] , -stacked_unique[:, 2] ))
        return x, y, z
    
if __name__ == "__main__":
    fig = plt.figure()
    ax = fig.add_subplot( projection='3d')
    poly = Polygon(3,vector3.Vector3(),ax)
    poly.show(alpha = 0.3, s=0.5, hide_bbox=False)
    plt.show()