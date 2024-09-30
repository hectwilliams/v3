import sys, os 
import matplotlib.axes
import numpy as np
import vector3  
import matplotlib.pyplot as plt 
import matplotlib
import objectv3
import time 
import matrix_4x3

class Circle(objectv3.Objectv3):
    def __init__(self, radius: np.float16 = 1.0, n: np.int32 = 50, center: np.ndarray = np.array([0.0,0.0,0.0],dtype=np.float32), axes: matplotlib.axes.Axes = None, **kwargs):
        super().__init__(n, center, axes)
        self.r = radius
        radius_sq = np.square(radius)
        m = matrix_4x3.Matrix4x3()
        m.set_translation(vector3.Vector3(*center))
        # object is zero origined then translated to center
        self.xx, self.yy = np.meshgrid( np.linspace(-6,6, dtype=np.float32, num=n), np.linspace(-6,6, dtype=np.float32, num=n), indexing='xy')
        radius_boundary = np.square(self.xx) + np.square(self.yy)
        indices_invalid = np.nonzero(radius_boundary > radius_sq)
        self.xx[*indices_invalid]= 0
        self.yy[*indices_invalid]= 0
        radius_boundary[*indices_invalid] = radius_sq
        radius_sq_minus_boundary =(radius_sq - radius_boundary)  
        self.zz = np.sqrt(np.where(radius_sq_minus_boundary<0, 1e-4, radius_sq_minus_boundary)) 
        self.load_mesh(self.xx, self.yy, self.zz)
        self.xform(m)

