import objectv3
import numpy as np
import matplotlib.pyplot as plt
from  mpl_toolkits.mplot3d.art3d import Line3D, Line3DCollection
from matplotlib.lines import Line2D
import vector3

class Polygon(objectv3.Objectv3):
    def __init__(self, num_sides, center, axes, radius=1.0, theta_offset=0.0, kx= 1.0, ky=1.0):
        super().__init__(center, axes)
        self.poly_num_sides = num_sides
        self.radius = radius
        self.center = center 
        if num_sides <= 2:
            raise ValueError('polygons requires at least 4 sides ')
        theta = np.deg2rad(np.linspace(theta_offset , 360, num=num_sides + 1))[:num_sides]
        # self.mesh = np.array([Triangle for i in range(n_sides-2)])
        self.poly_num_sides = num_sides-2
        alpha = ((np.pi/2) -  theta)
        x = kx + radius * np.cos(alpha)
        y = ky * radius * np.sin(alpha)
        z = np.zeros(shape=x.shape)
        self.load_mesh(x, y ,z) # change method new TODO 
        self.triangles_list = np.array([  [vector3.Vector3, vector3.Vector3,  vector3.Vector3] for _ in range(num_sides-2)])
        for i in range(num_sides -2):
            i_plus_1 = i + 1
            i_plus_2 = i + 2
            self.triangles_list[i][0] =  vector3.Vector3(x[0], y[0] , z[0])
            self.triangles_list[i][1] =  vector3.Vector3(x[i_plus_1], y[i_plus_1] , z[i_plus_1])
            self.triangles_list[i][2]  = vector3.Vector3(x[i_plus_2], y[i_plus_2] , z[i_plus_2])
    def connect_vertices(self, **kwargs):
        prev_ = -1
        next_ = 0
        self.line_connect = [Line3D for _ in range(self.pts.size)] 
        for i in range (self.pts.size):
            self.line_connect[i] = self.axes.plot(*zip(self.pts[prev_].to_numpy(), self.pts[next_].to_numpy())  , **kwargs)
            prev_ = next_
            next_ = prev_ + 1
    def disconnect_vertices(self):
        if self.line_connect:
            for lines in self.line_connect:
                for line in lines:
                    line.remove()
if __name__ == "__main__":
    fig = plt.figure()
    ax = fig.add_subplot( projection='3d')
    poly = Polygon(3,vector3.Vector3(),ax)
    poly.show(alpha = 0.3, s=0.5, hide_bbox=False)
    
    plt.show()