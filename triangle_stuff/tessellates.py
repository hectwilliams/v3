"""create tessellate plane using Triangle class"""
import matplotlib.pyplot as plt 
import matplotlib
import matplotlib.axes
import triangle
import numpy as np 
import vector3
from  mpl_toolkits.mplot3d.art3d import Line3DCollection, Path3DCollection, Text3D, Line3D
import tick

class Tessellates():
    def __init__(self,  axes: matplotlib.axes.Axes , triangle_per_cell = 1, layers = 1 , mode = 'load', num_nodes = 0, **kwargs):
        self.counter = tick.Tick()
        self.axes= axes

        if mode == 'test':
            if triangle_per_cell <= 0:
                raise ValueError('Each cell requires at least one triangle')
            if layers < 0:
                raise ValueError('layers must be greater than 0, 0th layer is the origin')
            self.rng =  np.random.Generator(np.random.PCG64(42)) if 'rng' not in kwargs else kwargs['rng']
            triangles_in_layer = lambda l: np.sum( np.array([-1, 0, 0, 1]) + 2.0 * np.float16(l) ).astype(dtype=np.int16)
            self.nodes = np.array([triangle for _ in range( triangle_per_cell* (1  + layers*triangles_in_layer(layers)  ) )]   )
            if triangle_per_cell == 1:
                v1,v2,v3,v4 = triangle.isosceles_triangle()
                self.nodes[self.counter.tick()] = triangle.Triangle(v1,v2,v3 ,axes=ax) 
                self.nodes[0].show(axes, 'vertex_name')
                self.mesh( self.nodes[0], layers)
            elif triangle_per_cell == 2:
                v1,v2,v3,v4 = triangle.obtuse_triangle(115)
                self.nodes[self.counter.tick()] = triangle.Triangle(v1,v2,v3 ,axes=ax) 
                self.nodes[self.counter.tick()] = triangle.Triangle(v2, v4, v3 ,axes=ax) 
                self.mesh( self.nodes[0], layers)
                self.mesh( self.nodes[1], layers)
            elif triangle_per_cell == 4:
                v1,v2,v3,v4 = triangle.obtuse_triangle(115)
                v_origin = (v1 + v2 + v3 + v4) / 4
                self.nodes[self.counter.tick()] = triangle.Triangle(v1,v_origin,v3 ,axes=ax) 
                self.nodes[self.counter.tick()] = triangle.Triangle(v2, v_origin, v1 ,axes=ax) 
                self.nodes[self.counter.tick()] = triangle.Triangle(v2, v4, v_origin ,axes=ax) 
                self.nodes[self.counter.tick()] = triangle.Triangle(v_origin, v4, v3 ,axes=ax) 
                self.mesh( self.nodes[0], layers)
                self.mesh( self.nodes[1], layers)
                self.mesh( self.nodes[2], layers)
                self.mesh( self.nodes[3], layers)
        if mode == 'load':
            self.rng =  np.random.Generator(np.random.PCG64(42)) if 'rng' not in kwargs else kwargs['rng']
            self.nodes = np.array([triangle.Triangle for _ in range( num_nodes )]   )
    
    def add_node(self, v1,v2,v3, axes):
        self.nodes[self.counter.tick()] = triangle.Triangle(v1,v2, v3 ,axes=axes)
    def hide(self):
        for node in self.nodes:
            node.unshow(mode='lines')
    def reveal(self):
        for node in self.nodes:
            node.uhow(mode='lines', ax=self.axes)
    def create_mesh(self, parent, layers):
        """used only in test gen mode"""
        if layers <= 0:
            raise ValueError('layer > 0 is required')
        # compute path 0
        for layer in range(1, layers + 1):
            for dir in [-1, 1]:
                v1 = parent.v1.to_numpy() + layer*dir*parent.e31
                v2 = parent.v2.to_numpy() + layer*dir*parent.e31
                v3 = parent.v3.to_numpy() + layer*dir*parent.e31
                self.nodes[self.counter.tick()] = triangle.Triangle(vector3.Vector3(*v1),vector3.Vector3(*v2),vector3.Vector3(*v3) ,axes=ax) 
                for j in range(1, layers):
                    v1_ = v1 + j*parent.e21
                    v2_ = v2 + j*parent.e21
                    v3_ = v3 + j*parent.e21
                    self.nodes[self.counter.tick()] = triangle.Triangle(vector3.Vector3(*v1_),vector3.Vector3(*v2_),vector3.Vector3(*v3_) ,axes=ax) 
                    v1_ = v1 - j*parent.e21
                    v2_ = v2 - j*parent.e21
                    v3_ = v3 - j*parent.e21
                    self.nodes[self.counter.tick()] = triangle.Triangle(vector3.Vector3(*v1_),vector3.Vector3(*v2_),vector3.Vector3(*v3_) ,axes=ax) 
            # # compute path 1
            for dir in [-1, 1]:
                v1 = parent.v1.to_numpy() + layer*dir*parent.e21
                v2 = parent.v2.to_numpy() + layer*dir*parent.e21
                v3 = parent.v3.to_numpy() + layer*dir*parent.e21
                self.nodes[self.counter.tick()] = triangle.Triangle(vector3.Vector3(*v1),vector3.Vector3(*v2),vector3.Vector3(*v3) ,axes=ax) 
                for j in range(1, layers + 1):
                    v1_ = v1 + j*parent.e31
                    v2_ = v2 + j*parent.e31
                    v3_ = v3 + j*parent.e31
                    self.nodes[self.counter.tick()] = triangle.Triangle(vector3.Vector3(*v1_),vector3.Vector3(*v2_),vector3.Vector3(*v3_) ,axes=ax) 
                    v1_ = v1 - j*parent.e31
                    v2_ = v2 - j*parent.e31
                    v3_ = v3 - j*parent.e31
                    self.nodes[self.counter.tick()] = triangle.Triangle(vector3.Vector3(*v1_),vector3.Vector3(*v2_),vector3.Vector3(*v3_) ,axes=ax) 

    def sweep(self,):
        for tri in self.nodes:
            lines = list(map( lambda x: x[0],  tri.get_lines() ))
            prev_lines_info = list(map(lambda ele: [ele.get_color(), ele.get_alpha()] ,    lines ))
            tri.update_line(color='red', alpha=1)
            plt.pause(0.01)
            tri.update_line(color=prev_lines_info[0][0] , alpha=prev_lines_info[0][1] )

    def test_random_pts(self):
        min_distance = np.finfo(np.float32).max
        cloeset_b = None 
        cloeset_node = None 
        pt = vector3.Vector3(  0.6989107852273501,  0.22167502757678514,  0.18477173225526122 )
        pt.rand(rng=rng) 
        # for node in self.nodes:
        #     b = node.coord_to_barycentric(pt)
        #     curr_distance = np.linalg.norm( np.abs (b - np.array([1/3, 1/3, 1/3]) )  )
        #     if curr_distance < min_distance:
        #         min_distance = curr_distance
        #         cloeset_b = b
        #         cloeset_node = node
        # coord = cloeset_node.barycentric_to_coord(*cloeset_b)
        # p = self.axes.scatter(*coord.to_numpy(), s=5, c='purple')
        # cloeset_node.highlight(None) 
        # plt.pause(0.8)
        # p.remove()
        # plt.pause(0.8)
        # time.sleep(0.5)
    def intersection(self):
        # origin of ray
        ray_origin = np.array([1.0,0.15,-0.5])
        # ray length and direction
        ray_delta = np.array([-1.5,1,0])
        # ray_delta = self.rng.random(size=(3))
        self.axes.quiver(*ray_origin, *ray_delta ,linewidth=0.5, arrow_length_ratio=0.11) # draw ray
        plt.pause(0.2)
        
        # triangle intersection by ray
        tri = self.nodes[17]
        # surface normal (unnormalized)
        n = tri.n 
        # compute d value for plane equation
        d = np.dot(n, tri.v1.to_numpy())
        
        ## ray triangle plane check
        ray_orgin_dot_n = ray_origin.dot(n)
        d_dot_n = ray_delta.dot(n)
        # ray parrallel to triangle plane
        if np.abs(d_dot_n) < 0.01:
            print ('ray is parrllel to triangle')
        # ray does not intersects with front of plane ( ray points in same direction as surface normal )
        if  (d_dot_n > 0):
            print ('ray does not intersect with front of plane')
        ## compute parametric point of intersection
        t = d - ray_orgin_dot_n
        # ray origin lies behind plane ( or back side of polygon which is incorrect; we wish to intersect to front only)
        if (t > 0):
            print ('ray origin lies behind the plane')
        t = t/d_dot_n
        # assert(t >= 0)
        if not t>=0:
            print ('t is invalid')
            return
        p = ray_origin + ray_delta * t
        # r y g  -->  draw intersect 
        ax.scatter(*p, color= ['red', 'yellow', 'green'][self.rng.integers(0,3)] , s=3)

if __name__ == '__main__':
    rng = np.random.Generator(np.random.PCG64(21))
    counter = 0
    ax = plt.subplot(projection='3d')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    ax.tick_params(axis='both', which='major', labelsize=5)
    widths = (-3,3)
    ax.set_xlim(*widths)
    ax.set_ylim(*widths)
    ax.set_zlim(*widths)
    ax.view_init(30, -50, 0)
    tessellate = Tessellates(axes = ax, triangle_per_cell = 2, layers=1, rng=rng, mode='test')
    plt.show()