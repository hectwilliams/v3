import numpy as np 
import vector3
import objectv3
import matrix_4x3

class Plane(objectv3.Objectv3):
    def __init__(self, n =50, center=np.random.random(size=(3)), axes=None, width=5) -> None:
        super().__init__(n, center, axes)
        xx, yy, zz = simple_zeroed_z_plane(self.n, width)
        self.load_mesh(xx, yy, zz)
        m = matrix_4x3.Matrix4x3()
        m.set_translation(vector3.Vector3(*center))
        self.xform(m)
        p = vector3.Vector3()
        p.rand() 
    def plane_normal(self):
        n= np.zeros(shape=(3))
        p = self.pts[-1]
        for i in range(self.pts.size):
            c = self.pts[i]
            n[0] += (p.z + c.z) * (p.y - c.y)
            n[1] += (p.x + c.x) * (p.z - c.z)
            n[2] += (p.y + c.y) * (p.x - c.x)
            p = c
        n = n/np.linalg.norm(n, ord=2)
        d = np.divide(np.array(list(map(lambda v3:v3.to_numpy()/np.linalg.norm(v3.to_numpy(), ord=2), self.pts))).sum(axis=0).dot(n), self.pts.size)
        d = d/np.linalg.norm(n, ord=2)
        return n, d
def simple_zeroed_z_plane(sq_matrix_n, width = 5):
    xx, yy = np.meshgrid(np.linspace(-width ,width, num=sq_matrix_n), np.linspace(-width,width, num=sq_matrix_n))
    zz = np.zeros(shape=xx.shape)
    return xx,yy,zz