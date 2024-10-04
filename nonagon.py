import numpy as np
import matplotlib.pyplot as plt 
import vector3
import time 
from  mpl_toolkits.mplot3d.art3d import Line3DCollection, Path3DCollection, Text3D, Line3D
import polygon

class Nonagon(polygon.Polygon):
    def __init__(self, center, axes, radius=1):
        super().__init__(num_sides=9, center=center, axes=axes, radius=radius, theta_offset=0)

if __name__ == "__main__":
    fig = plt.figure()
    ax = fig.add_subplot( projection='3d')
    nonagon = Nonagon(vector3.Vector3(),ax)
    nonagon.show(alpha = 0.3, s=0.5, hide_bbox=False)
    nonagon.remove_bbox()
    nonagon.connect_vertices()
    plt.show()