""" Bounding Box """
import sys 
import numpy as np 
import vector3
import matplotlib.pyplot as plt 

class AABB():
    def __init__(self) -> None:
        # corner points 
        self.vmin = vector3.Vector3()
        self.vmax = vector3.Vector3()
        self.box_vertices = np.array([vector3.Vector3() for _ in range(8)])
        self.plot_buffer = []
    def empty(self)-> None:
        big_number = np.finfo(np.float64).max
        self.vmin.x = self.vmin.y = self.vmin.z = big_number
        self.vmax.x = self.vmax.y = self.vmax.z = -big_number
    def acquire(self, data: np.ndarray, axis = 0):
        """set min max for axis"""
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
 
    def __repr__(self) -> str:
        return ('{}\n{}\n').format(self.vmax, self.vmin)
    def box(self, ax):
        """plot bounding box"""
        # clear bounding box 
        while len(self.plot_buffer):
            lines = self.plot_buffer.pop()
            lines[0].remove()

        # draw bounding box
        set_vertices(self.vmin, self.vmax, self.box_vertices) # 8 points required for bbox 
        line_map = [
            [0,1], 
            [1,3], 
            [2,3], 
            [0,2] ,
            [0,4],
            [4,6],
            [2,6],
            [4,5],
            [6,7],
            [5,7],
            [1,5],
            [5,7],
            [3,7],
            [1,3]
        ]
        for a, b in line_map:
            v_a = self.box_vertices[a]
            v_b = self.box_vertices[b]
            ln = ax.plot([v_a.x, v_b.x] , [v_a.y, v_b.y], [v_a.z, v_b.z]) 
            self.plot_buffer.append(ln)

    def rotate(self, m, ax):
        v_matrix = np.array(list(map(lambda v: [v.x, v.y, v.z], self.box_vertices)))
        v_matrix = np.matmul(v_matrix, m)
        print(v_matrix)
        for i in range(8):
            self.box_vertices[i].x = v_matrix[i][0]
            self.box_vertices[i].y = v_matrix[i][1]
            self.box_vertices[i].z = v_matrix[i][2]
        self.vmin.x, self.vmax.x = v_matrix[:,0].min(), v_matrix[:,0].max()
        self.vmin.y, self.vmax.y = v_matrix[:,1].min(), v_matrix[:,1].max()
        self.vmin.z, self.vmax.z = v_matrix[:,2].min(), v_matrix[:,2].max()
        self.box(ax)

def set_vertices(vmin, vmax, vertcies):
    """ using vmax and vmax vector assign 8 points for bounding box"""
    print(vmin)
    print(vmax)
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