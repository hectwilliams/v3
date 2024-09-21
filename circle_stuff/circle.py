import sys, os 
import matplotlib.axes
import numpy as np
import vector3 # PYTHONPATH 
import matplotlib.pyplot as plt 
import matplotlib
import objectv3
import time 
import matrix_4x3

class Circle(objectv3.Objectv3):
    def __init__(self, radius: np.float16 = 1.0, n: np.int32 = 50, center: np.ndarray = np.array([0.0,0.0,0.0],dtype=np.float32), axes: matplotlib.axes.Axes = None):
        super().__init__(n, center, axes)
        self.r = radius
        radius_sq = np.square(radius)
        m = matrix_4x3.Matrix4x3()
        m.set_translation(vector3.Vector3(*center))
        # object is zero origined
        xx, yy = np.meshgrid( np.linspace(-6,6, dtype=np.float32, num=n), np.linspace(-6,6, dtype=np.float32, num=n), indexing='xy')
        radius_boundary = np.square(xx) + np.square(yy)
        indices_invalid = np.nonzero(radius_boundary >= radius_sq)
        xx[*indices_invalid]= 0
        yy[*indices_invalid]= 0
        radius_boundary[*indices_invalid] = radius_sq
        radius_sq_minus_boundary =radius_sq - radius_boundary
        zz = np.sqrt(np.where(radius_sq_minus_boundary<0, 1e-4, radius_sq_minus_boundary)) 
        self.load_mesh(xx, yy, zz)
        self.xform(m)
if __name__ == '__main__':
    rng = np.random.Generator(np.random.PCG64(42))
    ax = plt.subplot(projection='3d')
    width = 4
    ax.set_xlim(-width, width)
    ax.set_ylim(-width, width)
    ax.set_zlim(-width, width)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    radius = 1.9510351886538364 
    center = np.array( [1.9512447 , 1.5222794  , 1.57212861] )
    for _ in range(10):
        center = rng.normal(0, 2, size=(3))
        circle1 = Circle(radius = rng.normal(), center=center)
        circle1.draw(dict(color='blue', alpha=0.4))
        center = rng.normal(0, 2, size=(3))
        circle2 = Circle(radius = rng.normal(), center=center) 
        circle2.draw(dict(color='yellow', alpha=0.4))
        plt.pause(0.2) 
        time.sleep(0.4)
        circle1.undraw()
        circle2.undraw()
    plt.show()


