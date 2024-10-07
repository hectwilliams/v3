import numpy as np
import matplotlib.pyplot as plt 
import vector3
import polygon

class Octagon(polygon.Polygon):
    def __init__(self, axes, center = vector3.Vector3(), radius=1):
        super().__init__(num_sides=8, center=center, axes=axes, radius=radius, theta_offset=0)

if __name__ == "__main__":
    lwidth = 5
    fig = plt.figure()
    ax = fig.add_subplot( projection='3d')
    ax.set_xlim(-lwidth,lwidth); ax.set_ylim(-lwidth,lwidth); ax.set_zlim(-lwidth, lwidth)

    octagon = Octagon(vector3.Vector3(),ax)
    octagon.show(alpha = 0.3, s=0.5, hide_bbox=False)
    octagon.remove_bbox()
    octagon.connect_vertices_plot(c='black')
    octagon.show_mesh_plot()
    plt.show()