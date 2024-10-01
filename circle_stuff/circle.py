import sys, os 
import matplotlib.axes
import numpy as np
import vector3  
import matplotlib.pyplot as plt 
import matplotlib
import objectv3
import matrix_4x3

class Circle(objectv3.Objectv3):
    def __init__(self, radius: np.float16 = 1.0, n: np.int32 = 50, center: np.ndarray = np.array([0.0,0.0,0.0],dtype=np.float32), axes: matplotlib.axes.Axes = None, **kwargs):
        super().__init__(center, axes)
        self.r = radius
        radius_sq = np.square(radius)
        m = matrix_4x3.Matrix4x3()
        m.set_translation(vector3.Vector3(*center))
        # object is zero origined then translated to center
        xx, yy = np.meshgrid( np.linspace(-radius,radius, dtype=np.float32, num=n), np.linspace(-radius,radius, dtype=np.float32, num=n), indexing='xy')
        xx = xx.flatten()
        yy = yy.flatten() 
        u = radius_sq - (np.square(xx) + np.square(yy))
        indices = np.nonzero(u < 0)
        xx = np.delete(xx, indices)
        yy = np.delete(yy, indices)
        zz = np.sqrt(radius_sq - (np.square(xx) + np.square(yy))) 
        xx = np.hstack((xx, xx))
        yy = np.hstack((yy, yy))
        zz = np.hstack((zz, -zz)) # +- sqrt
        self.load_mesh(xx, yy, zz)
        self.xform(m)

def circle2d():
    """example of 2d circle"""
    x = np.linspace(-1, 1, num=1000)
    y_func = lambda x: np.sqrt(1.0 - x**2.0)
    j = 1.0 - x**2.0
    indices = np.nonzero(j < 0)
    print(indices)
    new_j = np.delete(j, indices)
    new_x = np.delete(x, indices)
    new_j = np.sqrt(new_j)
    plt.plot(new_x, new_j)
    new_j = -np.sqrt(new_j)
    plt.plot(new_x, new_j)
    plt.show()

if __name__ == '__main__':
    ax = plt.subplot(projection = '3d')
    circle = Circle()
    circle.show(ax)
    plt.show()
