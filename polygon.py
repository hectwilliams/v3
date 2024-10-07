import objectv3
import numpy as np
import vector3
import matplotlib.pyplot as plt
from  mpl_toolkits.mplot3d.art3d import Line3D
import trianglenode

class Polygon(objectv3.Objectv3):
    def __init__(self, num_sides, center, axes, radius=1.0, theta_offset=0.0, kx= 1.0, ky=1.0, xy_is_mesh_grid=False, mesh_mode = 0):
        super().__init__(center, axes)
        self.poly_num_sides = num_sides
        self.radius = radius
        self.center = center 
        if num_sides <= 2:
            raise ValueError('polygons requires at least 4 sides ')
        theta = np.deg2rad(np.linspace(theta_offset , 360, num=num_sides + 1))[:num_sides]
        self.poly_num_sides = num_sides
        alpha = ((np.pi/2) -  theta)
        x = kx * radius * np.cos(alpha)
        self.x = x 
        y = ky * radius * np.sin(alpha)
        self.y = y 
        z = np.zeros(shape=x.shape)
        self.z = z
        x = x.flatten()
        y = y.flatten()
        z = z.flatten()

        if not xy_is_mesh_grid:
            self.load_mesh(x, y ,z) # change method new TODO 
            triangulate_mesh(self, self.poly_num_sides, mesh_mode)

        if not xy_is_mesh_grid:
            """ data load input from subclass"""
            pass 
        # generate mesh (TODO Thread this operation)
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
    def toggle_mesh(self):
        if hasattr(self, 'mesh'):
            for node in self.mesh:
                node.toggle_node()
        
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
        
    def xform(self, m):
        self.renove_mesh_plot()
        self.disconnect_vertices()
        super().xform(m)
        self.mesh = mesh(self)

def mesh(polygon: Polygon)->np.ndarray:
    if hasattr(polygon, 'triangle_list'):
        return np.array( [ trianglenode.Trianglenode(polygon.triangle_list[i][0], polygon.triangle_list[i][1], polygon.triangle_list[i][2]  , polygon.axes) for i in range ( len(polygon.triangle_list)  )  ] )
    
def triangulate_mesh(polygon:Polygon, num_of_side, mode = 0):
    """ fanning style mesh """
    if mode == 0:
        polygon.triangle_list = np.array([  [vector3.Vector3, vector3.Vector3,  vector3.Vector3] for _ in range(num_of_side-2)])
        for i in range(num_of_side -2):
            i_plus_1 = i + 1
            i_plus_2 = i + 2
            polygon.triangle_list[i][0] =  vector3.Vector3(polygon.x[0],        polygon.y[0] ,        polygon.z[0])
            polygon.triangle_list[i][1] =  vector3.Vector3(polygon.x[i_plus_1], polygon.y[i_plus_1] , polygon.z[i_plus_1])
            polygon.triangle_list[i][2]  = vector3.Vector3(polygon.x[i_plus_2], polygon.y[i_plus_2] , polygon.z[i_plus_2])
    elif mode == 1:
        """ pizza syle mesh """
        polygon.triangle_list = np.array([  [vector3.Vector3, vector3.Vector3,  vector3.Vector3] for _ in range(num_of_side + 2)])
        prev = -3
        next = -2
        for i in range(num_of_side + 2  ):
            polygon.triangle_list[i][0] =  polygon.center
            polygon.triangle_list[i][1] =  vector3.Vector3(polygon.x[prev], polygon.y[prev] , polygon.z[prev])
            polygon.triangle_list[i][2]  = vector3.Vector3(polygon.x[next], polygon.y[next] , polygon.z[next])
            prev = next 
            next = next + 1
    else :
        raise ValueError("invalid mode")
if __name__ == "__main__":
    fig = plt.figure()
    ax = fig.add_subplot( projection='3d')
    poly = Polygon(3,vector3.Vector3(),ax)
    poly.show(alpha = 0.3, s=0.5, hide_bbox=False)
    
    plt.show()