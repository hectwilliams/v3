""" scatter plot 3d examples
    
    rotate about cardinal axis using quarternion

"""

import matplotlib.pyplot as plt 
import numpy as np 
import vector3
import quarternion
import math 
import matrix_4x3
import asyncio

async def draw_x_line(axes):
    n = 50
    for x,y,z in list( zip( np.linspace(stop=-1, start=1, num=n), np.zeros(n), np.zeros(n))):
        axes.scatter(x,y,z, marker='o', c='black', s=1.0, alpha=0.7)
        plt.pause(0.1)
        await asyncio.sleep(0.0)
async def rotate_cardinal(axes):
    """rotate point about x axis"""
    await asyncio.sleep(0.5)
    v = vector3.Vector3(0, 1, 1)
    m = matrix_4x3.Matrix4x3()
    theta = (60/360.0)*math.pi
    q = quarternion.Quarternion()
    q.set_to_rotate_about_x(theta)
    m.from_quarternion(q)
    while True:
        plt.pause(0.1)
        axes.scatter(v.x, v.y, v.z, marker='o', c='blue', s=1)
        v = matrix_4x3.vector_mult(v, m)
        await asyncio.sleep(0.0)
async def rotate_arbitrary_axis(axes, rng):
    """rotate point about arbitrary axis"""
    v = vector3.Vector3(1.5, 1, 1)
    v_start = vector3.Vector3(1.5, 1, 1)
    q = quarternion.Quarternion()
    theta = (30/360.0)*math.pi
    m = matrix_4x3.Matrix4x3()
    n = vector3.Vector3( abs(rng.normal() ) , abs(rng.normal()) , rng.normal())
    n.normalize()
    q.set_to_rotate_about_axis(n, theta)
    m.from_quarternion(q)
    while True:
        v = matrix_4x3.vector_mult(v, m)
        axes.scatter(v.x, v.y, v.z, marker='x', c='red', s=2)
        plt.pause(0.1)
        print(v_start*v)
        await asyncio.sleep(0.0)
async def rotate_cardinal_2(axes):
    """Use sleep to interpolate rotation"""
    q1 = quarternion.Quarternion()
    q2 = quarternion.Quarternion()
    q1.set_to_rotate_about_x(0.0)
    q2.set_to_rotate_about_x( (60/360.0) * math.pi )
    m = matrix_4x3.Matrix4x3()
    m.from_quarternion(q1)
    q = quarternion.slerp(q1, q2, 0.5)
    m.from_quarternion(q)
    v =vector3.Vector3(0, 1, 1)
    while True:
        v = matrix_4x3.vector_mult(v, m)
        axes.scatter(v.x, v.y, v.z, marker='*', c='green', s=2)
        plt.pause(0.1)
        await asyncio.sleep(0.1)
rng = np.random.Generator(np.random.PCG64(242))
fig = plt.figure() 
ax = fig.add_subplot(projection='3d')
ax.set_xlabel('x label')
ax.set_ylabel('y label')
ax.set_zlabel('z label')
ax.set_xlim(-3, 3)
ax.set_ylim(-3, 3)
ax.set_zlim(-3, 3)
plt.ion()
plt.show()
loop = asyncio.new_event_loop() 
t1 = loop.create_task(draw_x_line(ax))
t2 = loop.create_task(rotate_cardinal(ax))
t4= loop.create_task(rotate_cardinal_2(ax))
t3 = loop.create_task(rotate_arbitrary_axis(ax, rng))
loop.run_forever()

