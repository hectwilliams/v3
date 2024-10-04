import decagon
import vector3
import matplotlib.pyplot as plt 
import quarternion
import matrix_4x3
import numpy as np 

if __name__ == '__main__':
    fig = plt.figure()
    ax = fig.add_subplot( projection='3d')
    common_width_limit = (-2,2)
    ax.set_xlim(*common_width_limit ); ax.set_ylim(*common_width_limit );ax.set_zlim(*common_width_limit )
    ax.axis('off')
    deca = decagon.Decagon(vector3.Vector3(),ax)
    deca.show(alpha = 0.3, s=0.5, hide_bbox=False)
    deca.remove_bbox()
    q = quarternion.Quarternion()
    m = matrix_4x3.Matrix4x3()
    deg = 0

    while True:
        if deg == 360:
            deg = 0
        dgon = decagon.Decagon(vector3.Vector3(),ax)
        m.setup_rotate_cardinal(3, np.deg2rad(deg))
        dgon.xform(m)
        dgon.show(hide_bbox=True, color='black')
        plt.pause(0.001)
        dgon.unshow()
        del dgon
        deg += 5