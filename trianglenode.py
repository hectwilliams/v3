
import numpy as np
import vector3

class Trianglenode():
    def __init__(self, v1,v2,v3, axes):
        self.show_vertex_name = False 
        self.show_lengths = False 
        self.show_normal= False
        self.show_vertex_node = False 
        self.show_lines = False
        self.line_connect = False 
        self.axes = axes

        self.v1 = v1
        self.v2 = v2
        self.v3 = v3
        
        self.center = ((self.v1 + self.v2 + self.v3 )/3.0) 
        
        self.e21 = self.v2 - self.v1    
        self.e12 = self.v1 - self.v2
        self.l1 =  np.linalg.norm(self.e21.to_numpy(), ord=2)

        self.e32 = self.v3 - self.v2
        self.e23 = self.v2 - self.v3
        self.l2 =  np.linalg.norm(self.e32.to_numpy(), ord=2)

        self.e13 = self.v1 - self.v3
        self.e31 = self.v3 - self.v1
        self.l3 = np.linalg.norm(self.e13.to_numpy())

        # collinear (parallel vector) test
        assert(np.linalg.norm(np.cross(self.e32.to_numpy(), self.e21.to_numpy()) ) ) # e21 x e32 
        assert(np.linalg.norm(np.cross(self.e32.to_numpy(), self.e13.to_numpy()) ) ) # e13 x e32
        assert(np.linalg.norm(np.cross(self.e21.to_numpy(), self.e13.to_numpy()) ) ) # e13 x e21
        
        cos_theta_1 = ((np.square(self.l2) + np.square(self.l3))  - np.square(self.l1) ) / (2 * self.l2 * self.l3 ) # angle eating line e32 (i.e. opposite of l1)
        self.theta_1 = np.acos(cos_theta_1)
        cos_theta_2 = ((np.square(self.l1) + np.square(self.l3))  - np.square(self.l2) ) / (2 * self.l1 * self.l3 ) # angle eating line e13
        self.theta_2 = np.acos(cos_theta_2)
        cos_theta_3 = ((np.square(self.l1) + np.square(self.l2))  - np.square(self.l3) ) / (2 * self.l1 * self.l2 ) # angle eating line e21
        self.theta_3 = np.acos(cos_theta_3)
        self.triangle_type = classify (self.theta_1, self.theta_2, self.theta_3)
        self.perimeter = self.l1 + self.l2 + self.l3

        e21xe32 = np.cross(self.e32.to_numpy() , self.e21.to_numpy())
        self.area =  np.linalg.norm(e21xe32) / 2
        self.v4 = self.e32 + self.v1 # final vectices to create parralelogram 
        self.e43 = self.v4 - self.v3 
        self.n = vector3.Vector3(*e21xe32) # e21 x e32 (np.cross uses RHS so swap inputs)
        self.n_norm = vector3.Vector3( *(e21xe32 / np.linalg.norm(self.n.to_numpy()) )) # e21 x e32 (np.cross uses RHS so swap inputs)
        
    def plot_normal(self):
        self.plt_normal = self.axes.quiver(*self.center.to_numpy(), *self.n_norm.to_numpy())
    def remove_normal(self):
        if self.plt_normal:
            self.plot_normal.remove()
    def plot_node (self, **kwargs) :
        self.line_connect = [
            self.axes.plot(*zip(self.v1.to_numpy() ,self.v2.to_numpy()),  **kwargs),
            self.axes.plot(*zip(self.v2.to_numpy() ,self.v3.to_numpy()),  **kwargs),
            self.axes.plot(*zip(self.v3.to_numpy() ,self.v1.to_numpy()),  **kwargs),
        ]
    def remove_node(self):
        if self.line_connect:
            for node_line3d in self.line_connect:
                for lines in node_line3d:
                    for line in lines:
                        line.remove() 
            self.line_connect = None 
    def toggle_node(self):
        if self.line_connect:
            for node_line3d in self.line_connect:
                for lines in node_line3d:
                    curr_state = lines.get_visible()
                    lines.set_visible( not curr_state)
        else:
            self.plot_node(c='black')
def classify(*angles_rad):
    res = ''
    for radians in angles_rad:
        deg = np.rad2deg(radians)
        if deg == 90 and res.find('right') == -1:
            res += 'right '
        if deg > 90 and res.find('obtuse') == -1:
            res += 'obtuse'
    return 'acute' if len(res) == 0 else res
