import numpy as np
import matplotlib.pyplot as plt
from  triangle_stuff.triangle import Triangle
import vector3

class BasicPolygon():
    def __init__(self, n_sides, axes, radius = 1, add_triangles= True):
        self.radius = radius 
        self.n = n_sides
        self.axes = axes
        if add_triangles and n_sides <=2:
            raise ValueError('Triangles requires 4 sides')
        theta = np.deg2rad(np.linspace(0 , 360, num=n_sides + 1))[:n_sides]
        self.mesh = [Triangle for i in range(n_sides-2)]
        alpha = ((np.pi/2) -  theta)
        x = radius * np.cos(alpha)
        y = radius * np.sin(alpha)
        z = np.zeros(shape=x.shape)
        for i in range(n_sides -2):
            i_plus_1 = i + 1
            i_plus_2 = i + 2
            v1 = vector3.Vector3(x[0], y[0] , z[0] )
            v2 = vector3.Vector3(x[i_plus_1], y[i_plus_1] , z[i_plus_1] )
            v3 =vector3.Vector3(x[i_plus_2], y[i_plus_2] , z[i_plus_2] )
            self.mesh[i] = Triangle( v1, v2, v3, axes=axes)

    def enable_mesh(self):
        for node in self.mesh:
            node.show(self.axes,)
    def highlight(self):
        for node in self.mesh:
            node.highlight(seconds=0.5)
    def disable_mesh(self):
        for node in self.mesh:
            node.unshow()

if __name__ == '__main__':
    ax = plt.subplot(projection='3d')
    for s in range(3, 100):
        poly = BasicPolygon(n_sides=s, axes=ax)
        poly.enable_mesh()
        poly.highlight()
        poly.disable_mesh()
plt.show()