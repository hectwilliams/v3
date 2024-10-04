import numpy as np
import matplotlib.pyplot as plt 
import vector3
import time 
from  mpl_toolkits.mplot3d.art3d import Line3DCollection, Path3DCollection, Text3D, Line3D
import polygon
import quarternion
import matrix_4x3

class Decagon(polygon.Polygon):
    def __init__(self, center, axes, radius=1):
        super().__init__(num_sides=10, center=center, axes=axes, radius=radius, theta_offset=0)

if __name__ == "__main__":
    fig = plt.figure()
    ax = fig.add_subplot( projection='3d')
    decagon = Decagon(vector3.Vector3(),ax)
    decagon.show(alpha = 0.3, s=0.5, hide_bbox=False)
    decagon2 = Decagon(vector3.Vector3(),ax)

    decagon.remove_bbox()
    # sqaure.connect_vertices()

    q = quarternion.Quarternion()
    m = matrix_4x3.Matrix4x3()

    while True:
        if deg == 360:
            deg = 0
        dgon = Decagon(vector3.Vector3(),ax)
        m.setup_rotate_cardinal(3, np.deg2rad(deg))
        dgon.xform(m)
        dgon.show(hide_bbox=True, color='black')
        plt.pause(0.001)
        dgon.unshow()
        del dgon

        deg += 5

    plt.show()