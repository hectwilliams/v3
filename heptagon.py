import numpy as np
import matplotlib.pyplot as plt 
import vector3
import polygon

class Heptagon(polygon.Polygon):
    def __init__(self, center, axes, radius=1):
        super().__init__(num_sides=7, center=center, axes=axes, radius=radius, theta_offset=0)

if __name__ == "__main__":
    fig = plt.figure()
    ax = fig.add_subplot( projection='3d')
    heptagon = Heptagon(vector3.Vector3(),ax)
    heptagon.show(alpha = 0.3, s=0.5, hide_bbox=False)
    heptagon.remove_bbox()
    heptagon.connect_vertices()
    plt.show()