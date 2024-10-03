import matrix_4x3
import objectv3
import numpy as np 
import vector3

class Plane(objectv3.Objectv3):
    def __init__(self, axes, center=vector3.zero_origin, length=5, width=5, height=5, plane_id = 'xy') -> None:
        """ 
            Generate a plane ( square plane are the default )
            Args:
                axes - figure to plot object 
                center - zero origin of type Vector3
                length - length of plane
                width - width of plane
                height = height of plane 
                plane_id = plane where object lives
        """
        super().__init__(center, axes)
        self.length = length 
        self.width = width 
        self.height = height
        self.plane_id = plane_id
        # y = np.linspace(-length, length)
        # x = np.linspace(-width, width)
        # z = np.linspace(-height, height)

        # if plane_id == 'xy':
        #     xx, yy = np.meshgrid(x, y)
        #     zz = np.zeros(shape=xx.shape)
        # elif plane_id == 'yz':
        #     yy, zz = np.meshgrid(x, y)
        #     xx = np.zeros(shape=yy.shape)
        # elif plane_id == 'xz':
        #     xx, zz = np.meshgrid(x, y)
        #     yy = np.zeros(shape=xx.shape)

        if plane_id == 'xy':
            v1 = vector3.Vector3(-length,0,0)
            v2 = vector3.Vector3(-length,width,0)
            v3 = vector3.Vector3(length,width,0)
            v4 = vector3.Vector3(length,0,0)
        elif plane_id == 'yz':
            v1 = vector3.Vector3(0, -length, 0)
            v2 = vector3.Vector3(0, -length,width)
            v3 = vector3.Vector3(0, length,width)
            v4 = vector3.Vector3(0,length,0)
        elif plane_id == 'xz':
            v1 = vector3.Vector3(-length,  0, 0)
            v2 = vector3.Vector3( -length, 0, width)
            v3 = vector3.Vector3( length,  0, width)
            v4 = vector3.Vector3( length,  0, 0)
        else:
            raise RuntimeWarning('invalid plane_id ')
        
        move = np.array([5, 1, -2])
        self.load_mesh  (  np.array( [v1.x, v2.x, v3.x, v4.x] ), np.array( [v1.y, v2.y, v3.y, v4.y] ), np.array( [v1.z, v2.z, v3.z, v4.z] )   )
        m = matrix_4x3.Matrix4x3()
        m.set_translation(vector3.Vector3(*move))
        self.xform(m)
        self.n, self.n_unorm= self.plane_normal()
        self.d = np.dot(self.pts[np.random.randint(low=0, high=self.pts.size)].to_numpy(), self.n_unorm )


 
    def plane_normal(self ):
        n= np.zeros(shape=(3))
        p = self.pts[-1]
        for i in range(self.pts.size):
            c = self.pts[i]
            n[0] += (p.z + c.z) * (p.y - c.y)
            n[1] += (p.x + c.x) * (p.z - c.z)
            n[2] += (p.y + c.y) * (p.x - c.x)
            p = c
        n_unnormalized = n
        n = n/np.linalg.norm(n, ord=2)
        return n, n_unnormalized 
    def copy(self):
        return Plane(self.axes, self.center, self.length, self.width,  self.height, self.plane_id)
    def show(self, axes) :
        """redraw plane lines if moved"""
        super().show(self.axes) 
        self.border = [
            self.axes.plot(*zip(self.pts[0].to_numpy(), self.pts[1].to_numpy()), c='black' ),
            self.axes.plot(*zip(self.pts[1].to_numpy(), self.pts[2].to_numpy()), c='black'),
            self.axes.plot(*zip(self.pts[2].to_numpy(), self.pts[3].to_numpy()), c='black'),
            self.axes.plot(*zip(self.pts[3].to_numpy(), self.pts[0].to_numpy()), c='black')
        ]
        # self.border2 = axes.quiver(*self.center.to_numpy(), *self.n)
    def unshow(self) :
        super().unshow()
        if self.border:
            for border in self.border:
                for line in border:
                    line.remove() 
        # self.border2.remove()
    def xform(self, m):
        super().xform(m)
        self.n, self.n_unorm= self.plane_normal()
        self.d = np.dot(self.pts[np.random.randint(low=0, high=self.pts.size)].to_numpy(), self.n_unorm )
