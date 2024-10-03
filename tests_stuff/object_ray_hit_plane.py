"""test - object ray intersecting plane"""
import vector3
import numpy as np 
import matplotlib.pyplot as plt 
import matrix_4x3
import plane_stuff.plane 
import circle_stuff.circle
import geometric_tests
import  triangle_stuff.tessellates
import sys 

if __name__ == '__main__':
    ax = plt.subplot(projection='3d')
    some_plane =  plane_stuff.plane.Plane(ax, plane_id='yz', center=vector3.Vector3(5,5,0))
    some_plane.show(ax)
    some_plane.bbox.remove_touch_points()
    entered = False
    circle = circle_stuff.circle.Circle(n = 10, axes=ax)
    circle.bbox.enable_touch_points(ax)
    plt.pause(0.2)
    m = matrix_4x3.Matrix4x3()
    y = np.linspace(0,10, 500)
    x = np.zeros(shape=y.shape)
    z = np.zeros(shape=x.shape)

    for i in range(y.size):
        circle.show(ax)
        arr = geometric_tests.intersection_bbox_ray_plane(circle, some_plane)
        if not arr and entered:
            break
        else:
            entered= True
            for p in arr:
                pad = ax.scatter(*p, color='pink')    
                plt.pause(0.1)
                pad.remove()
        circle.unshow()
        # tess.hide()
        m.set_translation(vector3.Vector3(x[i], y[i] ,z[i]),)
        circle.xform(m)
    circle.unshow()
    plt.show()