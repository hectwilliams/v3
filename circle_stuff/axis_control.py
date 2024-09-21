import numpy as np 
import matplotlib.pyplot as plt 
import time 
from mpl_toolkits.mplot3d import axes3d
import asyncio

def angle_norm(angle):
    return (angle + 180) % 360 - 180
def axis_control(ax):
    """ remove ticks and labels on axis"""
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_zticklabels([])
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])
async def azimuth(ax):
    ax.set_title('azimuth (heading)')
    elev = 0; roll = 0; azim = 0
    while True:
        azim = angle_norm((azim+1))
        ax.view_init(elev, azim, roll)
        await asyncio.sleep(0.2)
async def elevation(ax):
    ax.set_title('elevation (pitch)')
    elev = 0; roll = 0; azim = 0
    while True:
        elev = angle_norm((elev+1))
        ax.view_init(elev, azim, roll)
        await asyncio.sleep(0.2)
async def roll(ax):
    ax.set_title('roll (bank)')
    ax.set_xticks([])
    elev = 0; roll = 0; azim = 0
    while True:
        roll = angle_norm((roll+1))
        ax.view_init(elev, azim, roll)
        await asyncio.sleep(0.2)
async def update():
    while True:
        plt.draw()
        plt.pause(0.2)
        await asyncio.sleep(0.2)
        
fig = plt.figure() 
ax1 = fig.add_subplot(1, 3, 1, projection='3d')
ax2 = fig.add_subplot(1, 3, 2, projection='3d')
ax3 = fig.add_subplot(1, 3, 3, projection='3d')
axis_control(ax1)
axis_control(ax2)
axis_control(ax3)
loop = asyncio.new_event_loop()
t1 = loop.create_task(azimuth(ax1))
t3 = loop.create_task(elevation(ax2))
t4 = loop.create_task(roll(ax3))
t5 = loop.create_task(update())
loop.run_forever()
