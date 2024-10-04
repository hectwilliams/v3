import numpy as np
import matplotlib.pyplot as plt 
import vector3
import polygon

class Octagon(polygon.Polygon):
    def __init__(self, center, axes, radius=1):
        super().__init__(num_sides=8, center=center, axes=axes, radius=radius, theta_offset=0)

if __name__ == "__main__":
    fig = plt.figure()
    ax = fig.add_subplot( projection='3d')
    octagon = Octagon(vector3.Vector3(),ax)
    octagon.show(alpha = 0.3, s=0.5, hide_bbox=False)
    octagon.remove_bbox()
    octagon.connect_vertices()
    plt.show()