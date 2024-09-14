""" Bounding Box """
import numpy as np 
import vector3
import matplotlib.pyplot as plt 

class AABB():
    def __repr__(self) -> str:
        return ('{}\n{}\n').format(self.vmax, self.vmin)
    def __init__(self) -> None:
        self.vmin = vector3.Vector3()
        self.vmax = vector3.Vector3()
        self.box_vertices = np.array([vector3.Vector3() for _ in range(8)])
        self.plot_buffer = []
        self.vsize = np.zeros((3))
        self.center = np.zeros((3))
    def empty(self)-> None:
        big_number = np.finfo(np.float64).max
        self.vmin.x = self.vmin.y = self.vmin.z = big_number
        self.vmax.x = self.vmax.y = self.vmax.z = -big_number
    def is_empty(self)->bool:
        if self.vmin.x > self.vmax.x | self.vmin.y > self.vmax.y | self.vmin.z > self.vmax.z:
            return True 
        return False 
    def acquire(self, data: np.ndarray, axis = 0):
        """Set vmin vmax. Function is used to initialize the boudning box with a static points prior to any tranformations"""
        if axis == 0:
            if data.min() < self.vmin.x:
                self.vmin.x = data.min()
            if data.max() > self.vmax.x:
                self.vmax.x = data.max()
        elif axis == 1:
            if data.max()> self.vmax.y:
                self.vmax.y = data.max()
            if data.min()< self.vmin.y:
                self.vmin.y = data.min()
        elif axis == 2:
            if data.max()> self.vmax.z:
                self.vmax.z = data.max()
            if data.min()< self.vmin.z:
                self.vmin.z = data.min()
        self.size = self.vmax - self.vmin
        self.center = (self.vmax + self.vmin)/2
    def box(self, ax):
        """plot bounding box"""
        # draw bounding box
        set_vertices(self.vmin, self.vmax, self.box_vertices) # 8 points required for bbox 
        line_map = [ [0,1], [1,3], [2,3], [0,2],[0,4], [4,6], [2,6], [4,5],[6,7],[5,7],[1,5],[5,7],[3,7],[1,3]]
        for a, b in line_map:
            v_a = self.box_vertices[a]
            v_b = self.box_vertices[b]
            self.plot_buffer.append(ax.plot( [v_a.x, v_b.x] , [v_a.y, v_b.y], [v_a.z, v_b.z] , c='black'))
    def rotate(self, m, ax):
        # v_matrix = np.array(list(map(lambda v: [v.x, v.y, v.z], self.box_vertices)))

        # # compute xmin_new, xmax_new (use original bounding box limits to find new bound for x coordinate after transformation )
        # x_min = x_max= m[3][0]
        # x_min +=  (self.vmin.x if m[:,0][0] > 0  else self.vmax.x) * m[:,0][0]
        # x_max +=  (self.vmax.x if m[:,0][0] > 0  else self.vmin.x) * m[:,0][0]
        # x_min += (self.vmin.y if m[:,0][1] > 0  else self.vmax.y) * m[:,0][1]
        # x_max += (self.vmax.y if m[:,0][1] > 0  else self.vmin.y) * m[:,0][1]
        # x_min += (self.vmin.z if m[:,0][2] > 0  else self.vmax.z) * m[:,0][2]
        # x_max += (self.vmax.z if m[:,0][2] > 0  else self.vmin.z) * m[:,0][2]
        # y_min = y_max= m[3][1]
        # y_min +=  (self.vmin.x if m[:,1][0] > 0  else self.vmax.x) * m[:,1][0]
        # y_max +=  (self.vmax.x if m[:,1][0] > 0  else self.vmin.x) * m[:,1][0]
        # y_min += (self.vmin.y if m[:,1][1] > 0  else self.vmax.y) * m[:,1][1]
        # y_max += (self.vmax.y if m[:,1][1] > 0  else self.vmin.y) * m[:,1][1]
        # y_min += (self.vmin.z if m[:,1][2] > 0  else self.vmax.z) * m[:,1][2]
        # y_max += (self.vmax.z if m[:,1][2] > 0  else self.vmin.z) * m[:,1][2]
        # z_min = z_max= m[3][2]
        # z_min +=  (self.vmin.x if m[:,2][0] > 0  else self.vmax.x) * m[:,2][0]
        # z_max +=  (self.vmax.x if m[:,2][0] > 0  else self.vmin.x) * m[:,2][0]
        # z_min += (self.vmin.y if m[:,2][1] > 0  else self.vmax.y) * m[:,2][1]
        # z_max += (self.vmax.y if m[:,2][1] > 0  else self.vmin.y) * m[:,2][1]
        # z_min += (self.vmin.z if m[:,2][2] > 0  else self.vmax.z) * m[:,2][2]
        # z_max += (self.vmax.z if m[:,2][2] > 0  else self.vmin.z) * m[:,2][2]
        # self.vmax.x = x_max
        # self.vmax.y = y_max
        # self.vmax.z = z_max
        
        # self.vmin.x = x_min
        # self.vmin.y = y_min
        # self.vmin.z = z_min

        while len(self.plot_buffer):
            lines = self.plot_buffer.pop()
            for l in lines:
                l.remove()
        self.box(ax)

    def update_box(self,pts) ->None:
        data = np.array(list(map(lambda pt: [pt.x, pt.y, pt.z], pts ))).T
        self.empty()
        self.acquire(data[0], 0)
        self.acquire(data[1], 1)
        self.acquire(data[2], 2)

def set_vertices(vmin, vmax, vertcies):
    """ using vmax and vmax vector assign 8 points for bounding box"""
    #0
    vertcies[0].x = vmin.x
    vertcies[0].y = vmin.y 
    vertcies[0].z = vmin.z
    
    #1
    vertcies[1].x = vmax.x 
    vertcies[1].y = vmin.y 
    vertcies[1].z = vmin.z

    #2 
    vertcies[2].x = vmin.x 
    vertcies[2].y = vmin.y 
    vertcies[2].z = vmax.z

    #3 
    vertcies[3].x = vmax.x 
    vertcies[3].y = vmin.y 
    vertcies[3].z = vmax.z 

    #4 
    vertcies[4].x = vmin.x 
    vertcies[4].y = vmax.y 
    vertcies[4].z = vmin.z 

    #5 
    vertcies[5].x = vmax.x 
    vertcies[5].y = vmax.y 
    vertcies[5].z = vmin.z 

    #6 
    vertcies[6].x = vmin.x 
    vertcies[6].y = vmax.y 
    vertcies[6].z = vmax.z 
    
    #7 
    vertcies[7].x = vmax.x 
    vertcies[7].y = vmax.y 
    vertcies[7].z = vmax.z 