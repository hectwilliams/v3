import numpy as np
import matplotlib.tri as tri
import matplotlib.pyplot as plt
import asyncio
import sys 
async def shade_cell_left_diagnal(ax):
    """create 2d triangle mesh,shading two triangles per cell """
    tpcs = [] 
    while True:
        for v_x  in range(1, nsteps[0]):
            for v_y in range(0, nsteps[1]-1):
                rand_numbers = [rand_num for rand_num in  [np.random.normal(loc=0,scale = 2, size=3)]*2 ]
            # right triangle 
                t_right = tri.Triangulation(np.array([v_x, v_x-1, v_x  ] )/(nsteps[0]-1) , np.array([v_y, v_y+1, v_y+1])/(nsteps[0]-1))
                tpc1 = ax[0].tripcolor(t_right, rand_numbers[0], alpha=0.9, cmap='gray', shading='gouraud')  
            # left triangle 
                t_left = tri.Triangulation(np.array([v_x, v_x-1, v_x-1])/ (nsteps[0]-1), np.array([v_y, v_y, v_y+1])/ (nsteps[0]-1) )
                tpc2 = ax[0].tripcolor(t_left, rand_numbers[1], alpha=0.9, cmap='gray', shading='gouraud')  # Use 'flat' for flat shading
                tpcs.append(tpc1)
                tpcs.append(tpc2)
        plt.pause(0.2)
        await asyncio.sleep(0.2)
        while tpcs:
            tcp = tpcs.pop(0)
            tcp.remove()

async def shade_cell_bisectors(ax):
    """create 2d triangle mesh,shading 4 triangles per cell"""
    tpcs = [] 
    delta = 1/(nsteps[0]-1)
    mid_center = 1/ np.float64(2.0)
    mid_offset_x, mid_offet_y = [mid_center for _ in range(2)]  
    while True:
        for v_x  in range(1, nsteps[0]):
            for v_y in range(0, nsteps[1]-1):
                rand_numbers = [rand_num for rand_num in  [np.random.normal(loc=0,scale = 2, size=3)]*4 ]
            # bottom triangle 
                t_bottom = tri.Triangulation(np.array( [ v_x, (v_x-1), v_x - mid_offset_x ])*delta   , np.array( [ v_y, v_y, v_y + mid_offet_y] )*delta)
                tpc1 = ax[1].tripcolor(t_bottom, rand_numbers[0], alpha=0.9, cmap='gray', shading='gouraud')  
            # left triangle 
                t_left = tri.Triangulation(np.array([v_x-1, v_x-1, v_x-mid_offset_x] )*delta , np.array([v_y, v_y+1, v_y+mid_offet_y]) *delta)
                tpc2 = ax[1].tripcolor(t_left, rand_numbers[1], alpha=0.9, cmap='summer', shading='gouraud')  
            # top triangle 
                t_top = tri.Triangulation(np.array([v_x-1, v_x, v_x-mid_offset_x] )* delta , np.array([v_y+1, v_y+1, v_y+mid_offet_y])*delta)
                tpc3 = ax[1].tripcolor(t_top, rand_numbers[1], alpha=0.9, cmap='autumn', shading='gouraud')  
            # right triangle 
                t_right = tri.Triangulation(np.array([v_x, v_x, v_x-mid_offset_x] )* delta , np.array([v_y, v_y+1, v_y+mid_offet_y])*delta)
                tpc4 = ax[1].tripcolor(t_right, rand_numbers[1], alpha=0.9, cmap='winter', shading='gouraud')  
                for t in [tpc1,tpc2, tpc3, tpc4]:
                    tpcs.append(t)
        await asyncio.sleep(0.1)
        while tpcs:
            tcp = tpcs.pop(0)
            tcp.remove()


# define the vertices
origin=[0,0]
maximum=[1,1]
nsteps=[10,10]
x = np.linspace(origin[0], maximum[0], nsteps[0])  #
y = np.linspace(origin[1], maximum[1], nsteps[1])  #
xx, yy = np.meshgrid(x, y, indexing='xy')
fig,ax = plt.subplots(nrows=1, ncols=2)

# define the cell indexes
ci = np.arange(0, nsteps[0] - 1)
cj = np.arange(0, nsteps[1] - 1)
cii, cjj = np.meshgrid(ci, cj, indexing='ij')
corners = np.array([[0, 1, 0, 1], [0, 0, 1, 1]])
# [bottom_left, bottom_right, top_left, top_right] (9x3) Elements are cell vertices for a row of contiguious cells 
i = cii[:, :, None] + corners[None, None, 0, :, ]  
j = cjj[:, :, None] + corners[None, None, 1, :, ]  
# reshape the array so that its Nx4, either use -1 so
# numpy guesses the shape or define as i.shape[0]*i.shape[1]
gi_corners = (i+j*nsteps[0]).reshape(-1,4)

# flatten xx, yy and then stack vertically, then rotate
vertices = np.vstack([xx.flatten(),yy.flatten()])
vertices_transpose = vertices.T
tri1 = gi_corners[:,[0,1,3]]
tri2 = gi_corners[:,[1,2,3]] 
triangles = np.vstack([tri1,tri2])
ax[0].triplot(vertices_transpose[:,0],vertices_transpose[:,1], triangles[:])
ax[1].triplot(vertices_transpose[:,0],vertices_transpose[:,1], triangles[:])
plt.show()
plt.pause(0.2)

loop = asyncio.new_event_loop()
t1 = loop.create_task(shade_cell_left_diagnal(ax))
t3 = loop.create_task(shade_cell_bisectors(ax))
loop.run_forever() 
