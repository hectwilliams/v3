import vector3
import polygon
import numpy as np
import matplotlib.pyplot as plt 

class Circle(polygon.Polygon):
    """Circle"""
    def __init__(self, axes,center=vector3.Vector3(),radius=1.0, flat= False, mesh_mode = 0, use_mesh_grid = False):
        super().__init__(num_sides=50, center=center, axes=axes, radius=radius, theta_offset=0, xy_is_mesh_grid=use_mesh_grid, mesh_mode=mesh_mode, subclass_name = self.__class__.__name__) 
    def connect_vertices(self, **kwargs):
        "basic plane polygons use method"
        pass
    def disconnect_vertices (self, **kwargs):
        "basic plane polygons use method"
        pass
if __name__ == "__main__":
    fig = plt.figure()
    ax = fig.add_subplot( projection='3d')
    lwidth = 1
    ax.set_xlim(-lwidth,lwidth); ax.set_ylim(-lwidth,lwidth); ax.set_zlim(-lwidth, lwidth)
    ax.axis('off')
    circle = Circle(ax, mesh_mode = 1,  flat=0, use_mesh_grid=True)
    circle.show(alpha = 0.3, s=5.8, hide_bbox=False)
    circle.remove_bbox()
    circle.show_mesh_plot(c='blue', linewidth=0.2)
    plt.show()
  