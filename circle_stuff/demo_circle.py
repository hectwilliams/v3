""" demo circles"""

import matplotlib.pyplot as plt 
import numpy as np 
import circle 
import quarternion
import math 
import matrix_4x3
import multiprocessing as mp 
import ctypes
import time 
import aabb3
import objectv3
import vector3

def set_axis(ax):
    ax.set_xlabel('x label')
    ax.set_ylabel('y label')
    ax.set_zlabel('z label')
    ax.set_xlim(-axi_length, axi_length)
    ax.set_ylim(-axi_length, axi_length)
    ax.set_zlim(-axi_length, axi_length)
def fixed_circle(shared_mem, lock):
    global fig
    aabb3_obj= aabb3.AABB()
    N = M = 50 
    ax = fig.add_subplot(projection='3d')
    set_axis(ax)
    data = np.frombuffer(shared_mem.get_obj())
    aabb3_obj.acquire(data[0*M*N:1*M*N], 0)
    aabb3_obj.acquire(-data[0*M*N:1*M*N], 0)
    aabb3_obj.acquire(data[1*M*N:2*M*N], 1)
    aabb3_obj.acquire(-data[1*M*N:2*M*N], 1)
    aabb3_obj.acquire(data[2*M*N:3*M*N], 2)
    aabb3_obj.acquire(-data[2*M*N:3*M*N], 2)
    aabb3_obj.box(ax)
    with lock:
        ax.scatter( [data[0*M*N:1*M*N],  data[0*M*N:1*M*N] ], [data[1*M*N:2*M*N],   data[1*M*N:2*M*N] ], [data[2*M*N:3*M*N], -data[2*M*N:3*M*N] ],  marker='*',  c='blue',  s=1 , alpha=0.2)
    while True:
        plt.pause(0.1)
        time.sleep(1.0)

def rotate_cicle(shared_mem_c,shared_mem_s, lock):
    """Rotate circle using vectorized approach"""
    global fig
    N = M = 50 
    ax = fig.add_subplot( projection='3d')
    set_axis(ax)
    aabb3_obj= aabb3.AABB()
    q = quarternion.Quarternion() 
    m_ = matrix_4x3.Matrix4x3()
    # q.set_to_rotate_about_z(math.radians(30))
    n = vector3.Vector3(0.5,0.5, 0.7)
    n_origin = [0,0,0]
    n_end = np.array([n.x, n.y, n.z]) * 0.5
    q.set_to_rotate_about_axis(n, math.radians(30))
    m_.from_quarternion(q)
    m = m_.to_numpy()
    ax.quiver( *n_origin, *n_end, color='r') 
    data_c = np.frombuffer(shared_mem_c.get_obj())
    data_s = np.frombuffer(shared_mem_s.get_obj())
    scatter_c = ax.scatter( [data_c[0*M*N:1*M*N],  -data_c[0*M*N:1*M*N] ], [data_c[1*M*N:2*M*N],   -data_c[1*M*N:2*M*N] ], [data_c[2*M*N:3*M*N], -data_c[2*M*N:3*M*N] ],  marker='*',  c='green',  s=1 )
    scatter_s = ax.scatter( [data_s[0*M*N:1*M*N],  data_s[0*M*N:1*M*N] ], [data_s[1*M*N:2*M*N],   data_s[1*M*N:2*M*N] ], [data_s[2*M*N:3*M*N], -data_s[2*M*N:3*M*N] ],  marker='*',  c='green',  s=1 )
    aabb3_obj.acquire(data_c[0*M*N:1*M*N], 0)
    aabb3_obj.acquire(-data_c[0*M*N:1*M*N], 0)
    aabb3_obj.acquire(data_c[1*M*N:2*M*N], 1)
    aabb3_obj.acquire(-data_c[1*M*N:2*M*N], 1)
    aabb3_obj.acquire(data_c[2*M*N:3*M*N], 2)
    aabb3_obj.acquire(-data_c[2*M*N:3*M*N], 2)
    aabb3_obj.box(ax)
    plt.pause(0.1)
    
    while True:
        with lock:
            # aabb3_obj.rotate(m_.to_numpy_4x3(),ax)
            vert_updated_c = np.matmul(np.c_[ (data_c[0*M*N:1*M*N], data_c[1*M*N:2*M*N], data_c[2*M*N:3*M*N])] , m) # verties matrix * rotation matrix
            shared_mem_c[:] = np.hstack(( vert_updated_c[:,0], vert_updated_c[:,1], vert_updated_c[:,2] )) # update shared mem
            vert_updated_s = np.matmul(np.c_[ (data_s[0*M*N:1*M*N], data_s[1*M*N:2*M*N], data_s[2*M*N:3*M*N])] , m) # verties matrix * rotation matrix
            shared_mem_s[:] = np.hstack(( vert_updated_s[:,0], vert_updated_s[:,1], vert_updated_s[:,2] )) # update shared mem
        data_c = np.frombuffer(shared_mem_c.get_obj())
        data_s = np.frombuffer(shared_mem_s.get_obj())
        scatter_c.remove()
        scatter_c = ax.scatter( [data_c[0*M*N:1*M*N],  -data_c[0*M*N:1*M*N] ], [data_c[1*M*N:2*M*N],   -data_c[1*M*N:2*M*N] ], [data_c[2*M*N:3*M*N], -data_c[2*M*N:3*M*N] ],  marker='*',  c='green',  s=1 )
        scatter_s.remove()
        scatter_s = ax.scatter( data_s[0*M*N:1*M*N] , data_s[1*M*N:2*M*N], data_s[2*M*N:3*M*N],  marker='*',  c='green',  s=1 )
        plt.pause(0.1)
        time.sleep(0.1)

def rotate_cicle_v3(shared_mem_c,shared_mem_s, lock):
    global fig
    N = M = 50 
    ax = fig.add_subplot( projection='3d')
    set_axis(ax)
    data_c = np.frombuffer(shared_mem_c.get_obj())
    q = quarternion.Quarternion() 
    m_ = matrix_4x3.Matrix4x3()
    n_org = [0,0,0]
    n = vector3.Vector3(0.5,0.5, 0.7)
    t = vector3.Vector3(0, 0.1, 0)
    obj = objectv3.Objectv3()
    vectors = [None]* N*M*2

    q.set_to_rotate_about_axis(n, math.radians(10))
    m_.from_quarternion(q)
    ax.quiver( * n_org, *n.to_numpy(), color='r') 

    # store vectors in array 
    with lock:
        x_temp = data_c[0 : N*M]
        y_temp = data_c[N*M : 2*N*M]
        z_temp = data_c[2*N*M : 3*N*M]
        x = np.hstack((x_temp, x_temp))
        y = np.hstack((y_temp, y_temp))
        z = np.hstack((z_temp, -z_temp))
        obj.load_mesh(x, y ,z)
        obj.show(ax)
        plt.pause(0.1)
    time.sleep(0.5)
    count = 0
    with lock:
        while count < 5:
            m_.setup_translation(t)
            obj.xform(m_)
            time.sleep(0.2)
            obj.unshow()
            obj.show(ax)
            plt.pause(0.1)
            time.sleep(0.5)
            count += 1
        count = 0
        while count < 36:
            m_.setup_translation(vector3.Vector3(0.0,0.0,0.0))
            m_.from_quarternion(q)
            obj.xform(m_)
            obj.unshow()
            obj.show(ax)
            plt.pause(0.1)
            time.sleep(0.5)
            count += 1
    while True:
        time.sleep(0.2)
        plt.pause(0.1)

K, M, N = 3 , 50, 50 # array 
axi_length = 2
fig = plt.figure()
c = vector3.Vector3(0.0,0.0,0.0)
r = 1.0
l = 1.5

# circle gen
x = np.linspace(-l, l, M)
y = np.linspace(-l, l, N)
xx, yy = np.meshgrid(x, y, indexing='xy')
radius_boundary = (xx-c.x)*(xx-c.x) + (yy-c.y)*(yy-c.y)
exclude_indices = np.where(radius_boundary > r**2)
xx[exclude_indices[0], exclude_indices[1]] = 0
yy[exclude_indices[0], exclude_indices[1]] = 0
radius_boundary[exclude_indices[0], exclude_indices[1]] = r**2
zz = np.sqrt(r**2 - radius_boundary) 

#/\ symbol gen
xx_a, _ = np.meshgrid(x, y, indexing='xy')
yy_a = np.zeros(shape=xx_a.shape)
zz_a = xx_a.copy()
indices_left = np.nonzero(xx_a < 0)
indices_right = np.nonzero(xx_a >= 0)
zz_a[indices_left[0], indices_left[1]] = xx_a[ indices_left[0], indices_left[1] ] /(1.5)
zz_a[indices_right[0], indices_right[1]] = -xx_a[ indices_right[0], indices_right[1] ] /(1.5)
zz_a += 1

stacked_circle_data = np.stack((xx, yy, zz))
stacked_symbol_data = np.stack((xx_a, yy_a, zz_a))
# create shared buffered array object
shared_data_circle = mp.Array(typecode_or_type=ctypes.c_double,size_or_initializer = K*M*N)
shared_data_symbol = mp.Array(typecode_or_type=ctypes.c_double,size_or_initializer = K*M*N)
# fill buffered array with stacked data 
shared_data_circle[:] = stacked_circle_data.flatten() 
shared_data_symbol[:] = stacked_symbol_data.flatten()
# convert buffered array object to numpy 
original_array_circle = np.frombuffer(shared_data_circle.get_obj()).copy()
original_array_symbol = np.frombuffer(shared_data_symbol.get_obj()).copy()

if __name__ == '__main__':
    plock = mp.Lock()
    p1 = mp.Process(target=rotate_cicle_v3, args=(shared_data_circle, shared_data_symbol, plock))
    p2 = mp.Process(target=rotate_cicle, args=(shared_data_circle, shared_data_symbol, plock))
    cnt = mp.cpu_count()
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    
