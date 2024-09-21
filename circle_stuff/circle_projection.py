""" paint circle using projection"""

import numpy as np 
import quarternion
import matrix_4x3 
import matplotlib
import matplotlib.pyplot as plt 
import time 
import vector3

def point_projection(point):
    d = c_pt - point
    d_mag = np.linalg.norm(d, ord=2)
    b_mag = d_mag - radius 
    b = (b_mag/d_mag) * d
    return point + b

ax = plt.subplot(  projection='3d'  )
width_bounds = (-4, 4)
ax.set_xlim(*width_bounds)
ax.set_ylim(*width_bounds)
ax.set_zlim(*width_bounds)
ax.set_xticklabels([])
ax.set_yticklabels([])
ax.set_zticklabels([])
ax.set_xticks([])
ax.set_yticks([])
ax.set_zticks([])
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
    
n_samples = 100
radius = 1.0
radius_sq = radius**2
c_pt = np.array([0,0, 0], dtype=np.float32)
xx,yy = np.meshgrid( np.linspace(-1,1, dtype=np.float32, num=n_samples),np.linspace(-1,1, dtype=np.float32, num=n_samples), indexing='xy')
radius_boundary = (xx-c_pt[0])**2.0 + (yy-c_pt[1] )**2.0
indices_invalid = np.nonzero(radius_boundary > radius_sq)
xx[*indices_invalid]= 0
yy[*indices_invalid]= 0
radius_boundary[*indices_invalid] = radius_sq
zz = np.sqrt(radius_sq - radius_boundary) + c_pt[2]
ax.scatter(xx, yy, zz, s=1, c='black', alpha=0.11)
ax.scatter(xx, yy, -zz, s=1, c='black',  alpha=0.11)
# init point
origin = vector3.Vector3(0, 0, radius +2)
some_point_v = origin.to_numpy()
some_point_on_sphere = point_projection(some_point_v)
q_init = quarternion.Quarternion()
m = matrix_4x3.Matrix4x3()
m.zero_translation()
q_init.set_to_rotate_about_y(np.deg2rad(2))

for i in range(0, 180):
    scratchpad = [ax.scatter(*some_point_v, c='purple') , ax.scatter(*some_point_on_sphere, c='yellow')]
    lines = ax.plot(*zip(some_point_v, some_point_on_sphere), c='pink')
    # update variables
    q = quarternion.pow(q_init, i)
    print(f'[{i}] q = {q}')
    m.from_quarternion(q)
    some_point_v = np.matmul(origin.to_numpy(), m.to_numpy())
    some_point_on_sphere = point_projection(some_point_v)
    plt.pause(0.01)
    time.sleep(0.03)
    # clear current lines
    [scratchpad[i].remove() for i in range(2)  ]
    [lines[i].remove() for i in range(len(lines))  ]
plt.show()

