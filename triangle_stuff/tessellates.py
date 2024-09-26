"""create tessellate plane using Triangle class"""
import objectv3
import matplotlib.pyplot as plt 
import matplotlib
import matplotlib.axes
import triangle
import numpy as np 
import vector3
from  mpl_toolkits.mplot3d.art3d import Line3DCollection, Path3DCollection, Text3D, Line3D
import time

def cal_num_triangles(layers):
    count = 0 
    for layer_nth in range(2, layers + 1 ):
        cc = 0
        a = (layer_nth * 2) - 1
        b =  a - 1
        c =  b - 1
        cc = a + 2*b + c
        count += cc
    return count 

class Tessellates():
    def __init__(self, tri_main: triangle.Triangle, axes: matplotlib.axes.Axes , layers = 1 ):
        if layers <= 0:
            raise ValueError("layers argument must be > 0") 
        elif layers == 1:
            num_of_triangles = 1
        elif layers > 1:
            num_of_triangles = cal_num_triangles(layers) 
        self.axes= axes
        self.nodes = np.array([triangle for _ in range( num_of_triangles )])
        self.parent = tri_main
        tri_mirror = triangle.Triangle(v1 = tri_main.v3 , v2 = tri_main.v4, v3 = tri_main.v1, axes=axes)


        self.mesh(tri_main, layers)
        # self.sweep()
    def mesh(self, parent, layers):

        """create mesh of triangles and adds to node array"""
        curr_index = 0
        
        d = dict(is_tessellate=True)

        for i in range(1,layers):
            # start vertices to jump from origin, set/add vertices on path #
            v1_init =  i*parent.e21 + parent.v1.to_numpy()
            v2_init =  i*parent.e21 + parent.v2.to_numpy()
            v3_init =  i*parent.e21 + parent.v3.to_numpy()
            self.nodes[curr_index] = triangle.Triangle(v1=vector3.Vector3(*v1_init) ,  v2=vector3.Vector3(*v2_init), v3=vector3.Vector3(*v3_init), axes=self.axes, **d)
            self.nodes[curr_index].axes.text( *self.nodes[curr_index].center.to_numpy(), curr_index, fontsize=5)
            curr_index+=1

            for k in range(1, i):
                # current position jumped in previous logic
                for dir in [-1, 1]:
                    # current position jumped forward(forward direction relative to vertex direction)
                    v1 = dir*k*parent.e32 + v1_init
                    v2 = dir*k*parent.e32 + v2_init
                    v3 = dir*k*parent.e32 + v3_init
                    self.nodes[curr_index] = triangle.Triangle(v1=vector3.Vector3(*v1) ,  v2=vector3.Vector3(*v2), v3=vector3.Vector3(*v3), axes=self.axes, **d)
                    curr_index+=1

            # reset to start , repeat previous vertices computation in reverse direction
            v1_init =  -i*parent.e21 + parent.v1.to_numpy()
            v2_init =  -i*parent.e21 + parent.v2.to_numpy()
            v3_init =  -i*parent.e21 + parent.v3.to_numpy()
            self.nodes[curr_index] = triangle.Triangle(v1=vector3.Vector3(*v1_init) ,  v2=vector3.Vector3(*v2_init), v3=vector3.Vector3(*v3_init), axes=self.axes,  **d)
            curr_index+=1

            for k in range(1, i):
                for dir in [1, -1]:
                # current position jumped forward(forward direction relative to vertex direction)
                    v1 = dir* k*parent.e32 + v1_init
                    v2 = dir*k*parent.e32 + v2_init
                    v3 = dir*k*parent.e32 + v3_init
                    self.nodes[curr_index] = triangle.Triangle(v1=vector3.Vector3(*v1) ,  v2=vector3.Vector3(*v2), v3=vector3.Vector3(*v3),axes=self.axes,  **d)
                    curr_index+=1

            # # reset origin vertices to jump from origin , compute vertices for perpindicular path on plane #
            v1_init =  i*parent.e32 + parent.v1.to_numpy()
            v2_init =  i*parent.e32 + parent.v2.to_numpy()
            v3_init =  i*parent.e32 + parent.v3.to_numpy()
            self.nodes[curr_index] = triangle.Triangle(v1=vector3.Vector3(*v1_init) ,  v2=vector3.Vector3(*v2_init), v3=vector3.Vector3(*v3_init), axes=self.axes, **d)
            curr_index+=1
            for k in range(1, i+1):
                for dir in [1, -1]:
                    v1 = dir*k*parent.e21 + v1_init
                    v2 = dir*k*parent.e21 + v2_init
                    v3 = dir*k*parent.e21 + v3_init 
                    self.nodes[curr_index] = triangle.Triangle(v1=vector3.Vector3(*v1) ,  v2=vector3.Vector3(*v2), v3=vector3.Vector3(*v3), axes=self.axes, **d)
                    curr_index+=1

            v1_init =  -i*parent.e32 + parent.v1.to_numpy()
            v2_init =  -i*parent.e32 + parent.v2.to_numpy()
            v3_init =  -i*parent.e32 + parent.v3.to_numpy()
            self.nodes[curr_index] = triangle.Triangle(v1=vector3.Vector3(*v1_init) ,  v2=vector3.Vector3(*v2_init), v3=vector3.Vector3(*v3_init), axes=self.axes, **d)
            curr_index+=1
            for k in range(1, i+1):
                for dir in [1, -1]:
                    v1 = dir*k*parent.e21 + v1_init
                    v2 = dir*k*parent.e21 + v2_init
                    v3 = dir*k*parent.e21 + v3_init 
                    self.nodes[curr_index] = triangle.Triangle(v1=vector3.Vector3(*v1) ,  v2=vector3.Vector3(*v2), v3=vector3.Vector3(*v3),axes=self.axes, **d)
                    curr_index+=1

    def sweep(self):
        for tri in self.nodes:
            lines = list(map( lambda x: x[0],  tri.get_lines() ))
            prev_lines_info = list(map(lambda ele: [ele.get_color(), ele.get_alpha()] ,    lines ))
            # print(prev_lines_info)
            tri.update_line(color='green', alpha=1)
            plt.pause(0.01)
            tri.update_line(color=prev_lines_info[0][0] , alpha=prev_lines_info[0][1] )

    def test_random_pts(self):
        min_distance = np.finfo(np.float32).max
        cloeset_b = None 
        cloeset_node = None 
        pt = vector3.Vector3(  0.6989107852273501,  0.22167502757678514,  0.18477173225526122 )
        pt.rand(rng=rng) 
        for node in self.nodes:
            b = node.coord_to_barycentric(pt)
            curr_distance = np.linalg.norm( np.abs (b - np.array([1/3, 1/3, 1/3]) )  )
            if curr_distance < min_distance:
                min_distance = curr_distance
                cloeset_b = b
                cloeset_node = node
        coord = cloeset_node.barycentric_to_coord(*cloeset_b)
        p = self.axes.scatter(*coord.to_numpy(), s=5, c='purple')
        cloeset_node.highlight(None) 
        plt.pause(0.8)
        p.remove()
        plt.pause(0.8)
    def intersection(self):
        # generate ray
        global rng
        # start = np.array([rng.random() for i in range(3)])
        start = np.array([1.0,0,-0.5])
        end = np.array([-1.5,1,0])
        self.axes.quiver(*start, *end)
        plt.pause(0.2)
        
if __name__ == '__main__':
    rng = np.random.Generator(np.random.PCG64(21))
    counter = 0
    ax = plt.subplot(projection='3d')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    ax.tick_params(axis='both', which='major', labelsize=5)
    widths = (-1,2)
    ax.set_xlim(*widths)
    ax.set_ylim(*widths)
    ax.set_zlim(*widths)
    ax.view_init(16, -87, 0)
    tri = triangle.Triangle(create_rand_triange=True ,axes=ax) # master triangle
    coord = tri.barycentric_to_coord(0, 0, 1)
    # ax.scatter(*coord.to_numpy())
    # ax.scatter(*v.to_numpy(), c='pink', alpha=0.2)
    b = tri.coord_to_barycentric(coord)
    coord = tri.barycentric_to_coord(*b)
    # v = tri.barycentric_to_coord(*b)
    # ax.scatter(*coord.to_numpy())
    tessellate = Tessellates(tri, ax, layers=3)
    tessellate.intersection()
    for _ in range(10):
        tessellate.test_random_pts()

    plt.show()