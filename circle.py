import vector3
import polygon
import quarternion
import matrix_4x3
import numpy as np
import matplotlib.pyplot as plt 

USE_XY_GRID = False
class Circle(polygon.Polygon):
    def __init__(self, axes,center=vector3.Vector3(),radius=1.0, flat= False, mesh_mode = 0):
        print(mesh_mode)
        super().__init__(num_sides=50, center=center, axes=axes, radius=radius, theta_offset=0, xy_is_mesh_grid=USE_XY_GRID, mesh_mode=mesh_mode ) 
        if USE_XY_GRID:
            xx, yy = np.meshgrid(self.x, self.y)
            xx = xx.flatten() 
            yy = yy.flatten() 
            u = np.square(radius) - (np.square(xx) + np.square(yy) ) 
            negative_incides = np.nonzero( u < 0)
            xx = np.delete(xx, negative_incides)
            yy = np.delete(yy, negative_incides)
            zz =  np.sqrt(radius **2.0 - (xx**2.0 + yy**2.0) ) if not flat else np.zeros(shape=xx.shape)
            xx = np.hstack((xx, xx))
            yy = np.hstack((yy, yy))
            zz = np.hstack((zz, -zz)) # sqrt +-
            self.load_mesh(xx, yy, zz) 
    def connect_vertices(self, **kwargs):
        "basic plane polygons use method"
        pass
    def disconnect_vertices (self, **kwargs):
        "basic plane polygons use method"
        pass

if __name__ == "__main__":
    fig = plt.figure()
    ax = fig.add_subplot( projection='3d')
    lwidth = 5
    ax.set_xlim(-lwidth,lwidth); ax.set_ylim(-lwidth,lwidth); ax.set_zlim(-lwidth, lwidth)
    ax.axis('off')
    circle = Circle(vector3.Vector3(),ax, flat=True, mesh_mode = 1)
    circle.show(alpha = 0.3, s=0.8, hide_bbox=False)
    circle.remove_bbox()
    circle.show_mesh_plot(c='black')
    circle.show_triangulation_normal()

    plt.show()
    # circle.connect_vertices()
    # q = quarternion.Quarternion()
    # m = matrix_4x3.Matrix4x3()
    # deg = 0

    # while True:
    #     if deg == 360:
    #         deg = 0
    #     circle = Circle(vector3.Vector3(),ax)
    #     m.setup_rotate_cardinal(3, np.deg2rad(deg))
    #     circle.xform(m)
    #     circle.show(hide_bbox=True, color='black')
    #     plt.pause(0.001)
    #     circle.unshow()
    #     del circle
    #     deg += 5
    