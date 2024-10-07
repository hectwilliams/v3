import numpy as np
import matplotlib.pyplot as plt 
import vector3
import time 
from  mpl_toolkits.mplot3d.art3d import Line3DCollection, Path3DCollection, Text3D, Line3D
import polygon

class Triangle (polygon.Polygon):
    def __init__(self, axes,center= vector3.Vector3(), radius=1):
        super().__init__(num_sides=3, center=center, axes=axes, radius=radius)

def classify(*angles_rad):
    res = ''
    for radians in angles_rad:
        deg = np.rad2deg(radians)
        if deg == 90 and res.find('right') == -1:
            res += 'right '
        if deg > 90 and res.find('obtuse') == -1:
            res += 'obtuse'
    return 'acute' if len(res) == 0 else res

if __name__ == '__main__':
    ax = plt.subplot(projection='3d')
    triangle = Triangle( vector3.Vector3(), axes = ax)
    triangle.show()
    triangle.remove_bbox()
    triangle.disconnect_vertices()
    plt.show()  
