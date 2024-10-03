"""test - object ray intersecting plane"""
import vector3
import numpy as np 
import matplotlib.pyplot as plt 
import matrix_4x3
import plane_stuff.plane 
import circle_stuff.circle
import geometric_tests
import quarternion

if __name__ == '__main__':
    m = matrix_4x3.Matrix4x3()
    q =  quarternion.Quarternion()
    deg = 0
    entered = False 
    ax = plt.subplot(projection='3d')
    # plane
    some_plane =  plane_stuff.plane.Plane(ax, plane_id='yz', center=vector3.Vector3(5,5,0))
    some_plane.bbox.remove_touch_points()
    # circle 
    circle = circle_stuff.circle.Circle(n = 50, axes=ax)
    circle.show(ax)
    circle.bbox.enable_touch_points(ax)
    circle.remove_bbox()
    # axes 
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_zticklabels([])
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])
    ax.axis('off')
    # looping task
    while True:
        if deg == 360:
            deg = 0

        clone_plane = some_plane.copy()
        q.set_to_rotate_about_z(np.deg2rad(deg))
        m.from_quarternion(q)
        clone_plane.xform(m)
        clone_plane.show(ax)
        clone_plane.remove_bbox()
        arr = geometric_tests.intersection_bbox_ray_plane(circle, clone_plane)
        if not (not arr and entered):
            entered= True
            for p in arr:
                pad = ax.scatter(*p, color='red', s=1.5)    
                plt.pause(0.05)
                pad.remove()

        plt.pause(0.1)
        clone_plane.unshow()
        deg += 5
    

