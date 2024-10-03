import vector3
import numpy as np
import matplotlib.pyplot as plt
import time 
import circle_stuff.circle
import plane_stuff.plane
def closest_point_on_line():
    """ project point to closest distance on line (another point)"""
    N = 500
    ax = plt.subplot()
    y = np.zeros(shape=(10, N))
    n = np.array([1,1], dtype=np.float32)
    x = np.linspace(-3, 3, N)
    d = 2
    normalize(n)
    # some line
    y[d] = (d -  n[1]*x) / n[0]
    ax.scatter(x, y[d],  c='red', s=0.01)
    ax.quiver(x[70], y[d][70], n[0], n[1])
    # random points on 
    for q in np.random.standard_normal(size=(100, 2)):
        ax.scatter(*q, c='blue', alpha=0.4)
        q_prime = q + (d - q.dot(n))*n
        ax.plot( [ q[0], q_prime[0] ], [ q[1],  q_prime[1]  ] , linewidth=0.2)
        ax.scatter(*q_prime, c='orange', alpha=0.3, s=0.5)
    ax.set_title('points closest to line')
    plt.show()
def closest_point_on_plane():
    """ project point to closest distance on plane (another point)"""
    N = 100
    n = vector3.Vector3(1,1,1)
    n_org = vector3.Vector3(0,0,0)
    d = 2.0
    ax = plt.subplot(projection='3d')
    xx, yy = np.meshgrid(np.linspace(-5, 5, N), np.linspace(-5, 5, N), indexing='xy')
    zz = (d -(n.x*xx + n.y*yy)) / n.z
    
    n = n.to_numpy()
    normalize(n)
    print(n)
    ax.scatter(xx, yy, zz, alpha=0.31, s=0.1)
    ax.quiver(*n_org.to_numpy(), *n)
    ax.set_xlabel('x label')
    ax.set_ylabel('y label')
    ax.set_zlabel('z label')
    some_point = np.array([2, 2, 5])
    for _ in range(50):
        r = np.random.random()
        r_step = np.random.random()
        step = 2
        if r < 0.3:
            some_point[0] += step if r_step < 0.5 else -step
        elif r < 0.6:
            some_point[1] += step if r_step < 0.5 else -step
        else:
            some_point[2] += step if r_step < 0.5 else -step

        some_point_projection = some_point + (d - some_point.dot(n)) * n 
        p1 = ax.scatter(*some_point, c='pink')
        p2 = ax.scatter(*some_point_projection, c='purple')
        plt.pause(0.1)
        time.sleep(0.5)
        p1.remove()
        p2.remove()
    plt.show()
def closest_point_on_2d_cicle():
    ax = plt.subplot()
    ax.set_xlim(-2,2)
    ax.set_ylim(-2,2)
    radius = 0.5
    radius_sq = radius**2
    c_pt = np.array([0,0])
    xx, = np.meshgrid( np.linspace(-1,1, dtype=np.float32, num=300), indexing='xy')
    radius_boundary = (xx-c_pt[0])**2.0
    indices_x, = np.nonzero(radius_boundary > radius_sq)
    xx[indices_x] = 0 # remove/or zero positions that violate boundary
    radius_boundary[indices_x] = radius_sq # this will force the violators to origin
    yy =  np.sqrt(radius_sq  - radius_boundary) + c_pt[1]
    scatter_pt_size = 0.3
    ax.scatter(xx, yy, s=scatter_pt_size)
    ax.scatter(xx, -yy, s=scatter_pt_size)
    q = np.random.random(size=(2))# random point 
    p1= ax.scatter(*q, s=1, c='black')
    steps = 30
    for _ in range(steps):
        d = c_pt-q # distance from q to center of circle
        d_mag = np.linalg.norm(d, ord=2)
        b_mag = d_mag - radius # distance closest edge to q 
        b = (b_mag/d_mag)*d 
        q_new = q + b
        p2 = ax.scatter(*q_new, s=2, c='red')
        plt.pause(0.3)
        time.sleep(0.5)
        p1.remove()
        p2.remove() 
        q = rotate_pt(q, 5)
        p1 = ax.scatter(*q, s=2, c='black')
    plt.show()
def closest_point_on_ray():
    ax = plt.subplot() 
    ax.set_xlim(-5,5)
    ax.set_ylim(-6,6)
    p_org = np.zeros(shape=(2))
    p_end = np.array([0, 5])
    d = p_end.copy()
    normalize(d)
    ax.arrow(*p_org, *p_end, head_width=0.1, head_length=0.2, fc='blue', ec='blue', alpha=0.10)
    ax.quiver(*p_org, *d, linewidth=1.0)
    ax.text(*d,"d")
    for _ in range(40):
        q = np.random.normal(size=2)
        t = d.dot(q) 
        q_ = p_org + t*d
        pad = [ax.scatter(*q, c='pink') , ax.scatter(*q_, c='black')]
        lines =  ax.plot( [q[0], q_[0]], [q[1], q_[1]])
        plt.pause(0.1)
        time.sleep(0.2)
        [pad[i].remove() for i in range(2)]
        [lines[i].remove() for i in range(len(lines))]
    plt.show()
def intersection_two_rays_3d():
    ax = plt.subplot(projection='3d') 
    ax.set_xlim(-70,70); ax.set_ylim(-70,70); ax.set_zlim(-70,70)
    xx, yy = np.meshgrid(np.linspace(-70,70,100), np.linspace(-70,70,100))
    zz = np.zeros(xx.shape)
    quiver_settings = dict(linewidth=0.1, alpha=0.2)
    num_of_pts = 100
    s_pad = [None] * 7
    for _ in range(50):
        t_range = np.linspace(0,100, num_of_pts)
        d1 = np.random.random(size=(3) ) * 2.0
        d2 = np.random.random(size=(3) ) * 2.0
        p1_origin, p2_origin = [ np.random.randint(low=-10, high=10, size=(3)) for _ in range(2) ]
        normalize(d1)
        normalize(d2)
        # draw rays
        # ray 2
        s_pad[0] = ax.quiver(*p2_origin, *( p2_origin + (d2 * t_range[-1]) ) , linewidth=0.5, color='red')
        s_pad[4]= ax.quiver(  *( p2_origin + (-1 * d2 * t_range[-1]) ) , *( p2_origin + (d2 *2* t_range[-1]) ) , linewidth=0.2, color='red', alpha=0.4) # extend
        # ray 1
        s_pad[1] = ax.quiver(*p1_origin, *( p1_origin + d1 * t_range[-1] ) , linewidth=0.5, color='blue')
        s_pad[5] =  ax.quiver(  *( p1_origin + (-1 * d1 * t_range[-1]) ) , *( p1_origin + (d1 *2* t_range[-1]) ) , linewidth=0.2, color='blue', alpha=0.4) # extend 
        # intersection 1
        t1 = range_interesect_two_ray(p1_origin, p2_origin, d1, d2, 1)
        t2 = range_interesect_two_ray(p1_origin, p2_origin, d1, d2, 2)
        r1 = p1_origin + t1*d1 
        r2 = p2_origin + t2*d2
        s_pad[2] = ax.scatter(*r1, c='pink', alpha=0.3)
        s_pad[3] = ax.scatter(*r2, c='yellow', alpha=0.3)
        # skew 
        s_pad[6] = ax.plot( [r1[0], r2[0]] , [r1[1], r2[1]], [r1[2], r2[2]], c='rebeccapurple')
        plt.pause(0.3)
        time.sleep(0.5)
        [s_pad[i].remove() for i in range(6)]
        [s_pad[-1][i].remove() for i in range(len(s_pad[-1]))]
    plt.show()
def  compute_plane():
    lwidth = 5
    lwidth2 = 10
    num_points = 100
    ax = plt.subplot(projection='3d')
    ax.set_xlim(-lwidth*2,lwidth*2); ax.set_ylim(-lwidth*2,lwidth*2); ax.set_zlim(-lwidth, lwidth)
    xx, yy = np.meshgrid(np.linspace(-lwidth2 ,lwidth2, num=num_points), np.linspace(-lwidth2,lwidth2, num=num_points))
    zz = np.zeros(shape=xx.shape)
    ax.scatter(xx, yy, zz, alpha=0.1)
    # points on plane 
    p1 = np.array([3,2,0], dtype=np.float32)
    p2 = np.array([4,9,0], dtype=np.float32)
    p3 = np.array([9,3,0], dtype=np.float32)
    # edge 
    e3 = p2 - p1 
    e1 = p3 - p2
    e1_x_e3 = np.cross(e1,e3)
    n = e1_x_e3 / np.linalg.norm(e1_x_e3, ord=2)
    n_start = n.copy() 
    n_start[2] = 0
    c='purple'
    ax.scatter(*p1, c=c)
    ax.scatter(*p2, c=c)
    ax.scatter(*p3, c=c)
    ax.quiver(*n_start, *n)
    plt.show() 
def compute_best_fit_plane():
    length_xy = 20
    ax = plt.subplot(projection='3d'); 
    ax.set_zlim(-length_xy,length_xy)
    ax.set_xlim(-length_xy,length_xy)
    ax.set_ylim(-length_xy,length_xy)
    ax.view_init(70, -74, 0) # elev, azim, roll
    xx, yy = np.meshgrid(np.linspace(-length_xy,length_xy,100), np.linspace(-length_xy,length_xy,100))
    zz = (xx - yy)
    ax.scatter(xx, yy, zz, alpha=0.02)
    n = np.array( object=[0,0,0], dtype=np.float32)
    num_pts = 100
    pts = [None] * num_pts
    for i in range(num_pts):
        randx = np.random.randint(num_pts)
        randy = np.random.randint(num_pts)
        px = xx[randx][randy]
        py = yy[randx][randy]
        pz = zz[randx][randy]
        pts[i] = np.array([px, py, pz])
    p = pts[ num_pts - 1 ]
    for i in range(num_pts):
        ax.scatter(*pts[i], s=0.5)
        c = pts[i]
        n[0] += (p[2] + c[2]) * (p[1] - c[1])
        n[1] += (p[0] + c[0]) * (p[2] - c[2])
        n[2] += (p[1] + c[1]) * (p[0] - c[0])
        p = c
    normalize(n) 
    d = np.dot(np.sum(pts, axis=0), n) / (num_pts) 
    ax.scatter(xx, yy, zz, alpha=0.02)
    ax.quiver(* np.array([0,0,0], dtype=np.float32), *n, color='red')
    # random points not on plane project on plane 
    for _ in range(30):
        randx = np.random.randint(num_pts)
        randy = np.random.randint(num_pts)
        some_point = np.array([ xx[randx][randx], yy[randx][randy], 8])
        a = some_point.dot(n) - d
        p_plane = some_point - a*n
        pad = [ax.scatter(*p_plane) ,ax.scatter(*some_point)]
        plt.pause(0.14)
        time.sleep(0.4)
        [pad[i].remove() for i in range(2)]
    plt.show()
def closest_point_on_3d_cicle():
    ax = plt.subplot(  projection='3d'  )
    ax.set_xlim(-2,2)
    ax.set_ylim(-2,2)
    ax.set_zlim(-2,2)
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
    ax.scatter(xx, yy, zz, s=1, c='black', alpha=0.01)
    ax.scatter(xx, yy, -zz, s=1, c='black',  alpha=0.01)
    for _ in range(200):
        # some point
        some_point = np.random.normal(0, 1, size=(3) ) 
        d = c_pt - some_point
        d_mag = np.linalg.norm(d, ord=2)
        b_mag = d_mag - radius 
        b = (b_mag/d_mag) * d
        some_point_on_sphere = some_point + b
        scratchpad = [ax.scatter(*some_point, c='purple') , ax.scatter(*some_point_on_sphere, c='yellow')]
        lines = ax.plot(*zip(some_point, some_point_on_sphere), c='pink')
        plt.pause(0.0001)
        time.sleep(0.1)
        [scratchpad[i].remove() for i in range(2)  ]
        [lines[i].remove() for i in range(len(lines))  ]
    plt.show()
def intersection_two_circles():
    rng = np.random.Generator(np.random.PCG64(21))
    ax = plt.subplot(projection='3d')
    width = 6
    ax.set_xlim(-width, width)
    ax.set_ylim(-width, width)
    ax.set_zlim(-width, width)
    cs = circle_stuff.circle.Circle(radius = rng.random(dtype=np.float32), center = rng.normal( size=(3)),axes=ax )
    cs.draw(dict(color='yellow', alpha=0.7) )
    cont = 0
    for _ in range(40):
        cm = circle_stuff.circle.Circle(radius = rng.random(), center = rng.normal(0, 2, size=(3)) , axes=ax)
        cm.draw(dict(color='red', alpha=0.7)) 
        cs_out =  cs.c - cm.c
        pad1 = ax.quiver(*cm.c, *cs_out, color='pink', alpha=0.7)
        cm_out = rng.normal(0, 2, size=(3)) 
        pad2 = ax.quiver(*cm.c, *cm_out, color='orange', alpha=0.7)
        d = cm_out.copy()
        normalize(d)
        pad3 = ax.quiver(*cm.c, *d, color='black', alpha=0.8)
        e = cs.c - cm.c
        r = cm.r + cs.r 
        r_sq = np.square(r)
        e_dot_d = e.dot(d)
        e_dot_d_sq = np.square(e_dot_d)
        e_dot_e = e.dot(e)
        u = e_dot_d_sq + r_sq - e_dot_e
        if e_dot_d > 0 and u > 0:
            print('moving sphere will hit stationary sphere!')
            cont += 1
            t = e_dot_d - np.sqrt(u)
            q_pt = cm.c + t*d
            if cont == 2:
                new_circle = circle_stuff.circle.Circle(cm.r, cm.n, q_pt , axes=ax) 
                print( f'VALID {new_circle.r} \t {new_circle.c}')
                new_circle.draw(dict(color='purple', alpha=0.7))
                plt.show() # pause when found
        plt.pause(0.3)
        time.sleep(0.5)
        cm.undraw()
        pad1.remove()
        pad2.remove()
        pad3.remove()
def cloeset_point_to_aabb():
    global rng
    global ax
    width = 5 
    ax.set_xlim(-width, width)
    ax.set_ylim(-width, width)
    ax.set_zlim(-width, width)
    circle = circle_stuff.circle.Circle(radius=1.2, axes=ax)
    circle.show(ax)
    for _ in range(30):
        circle2 = circle_stuff.circle.Circle(radius=rng.random()*2, center= 4.0*rng.random(size=(3)))
        intersect_pt, is_intersecting = circle.intersect_bbox_test(circle2)
        circle2.show(ax, dict(color='orange'))
        tmp = ax.scatter(*intersect_pt.to_numpy())
        circle2.remove_bbox()
        if is_intersecting:
            print('intersects')
        plt.pause(0.3)
        time.sleep(0.5)
        tmp.remove()
        circle2.unshow()
    plt.show() 

def intersection_bbox_ray_plane(c, some_plane):
    data = []
    for plane ,a ,b  in [  ('xz', 'ymin' , 'ymax'), ('xy', 'zmin' , 'zmax') , ('yz', 'xmin' , 'xmax') ]:
        for side in [a,b]:
            p0 = c.bbox.faces[plane][side]['center'] # vector
            p0_dir = c.bbox.faces[plane][side]['n']   # numpy ( unormalized)
            
            p0 = p0.to_numpy()
            po_dot_n = p0.dot(some_plane.n_unorm)
            
            d_dot_n = p0_dir.dot(some_plane.n_unorm)
            if d_dot_n == 0:
                break
            t = (some_plane.d - po_dot_n) / d_dot_n
            if d_dot_n < 0 :
                p0_ray = p0 + t*p0_dir
                xz_bound_test = (plane == 'xz') and (p0_ray[0] <= some_plane.bbox.vmax.x and p0_ray[0] >= some_plane.bbox.vmin.x) and (p0_ray[2] <= some_plane.bbox.vmax.z and p0_ray[2] >= some_plane.bbox.vmin.z)
                xy_bound_test = (plane == 'xy') and (p0_ray[0] <= some_plane.bbox.vmax.x and p0_ray[0] >= some_plane.bbox.vmin.x) and (p0_ray[1] <= some_plane.bbox.vmax.y and p0_ray[1] >= some_plane.bbox.vmin.y)
                yz_bound_test = (plane == 'yz') and (p0_ray[1] <= some_plane.bbox.vmax.y and p0_ray[1] >= some_plane.bbox.vmin.y) and (p0_ray[2] <= some_plane.bbox.vmax.z and p0_ray[2] >= some_plane.bbox.vmin.z)
                if xz_bound_test or xy_bound_test or yz_bound_test:    
                    data.append(p0_ray)
    return data
def interesection_ray_and_plane():
    global ax
    global rng
    width = 10
    ax.set_xlim(-width, width)
    ax.set_ylim(-width, width)
    ax.set_zlim(-width, width)
    plane = plane_stuff.plane.Plane(axes=ax)
    normal = plane.plane_normal()
    d = plane.pts[20].to_numpy().dot( normal ) # dot product 
    for _ in range(20):
        po = vector3.Vector3() # random point 
        po.rand() 
        d_norm = rng.random(size=(3)) #direction of po
        po_dot_n = po.to_numpy().dot(normal)
        d_dot_n = d_norm.dot(normal)
        t = (d - po_dot_n) / d_dot_n
        po_intersect = po.to_numpy() + t*d_norm
        po_past = po.to_numpy() + -100*d_norm
        po_future = po.to_numpy() + 200*d_norm
        quiv1 = ax.quiver( *po_past, *po_future, color='brown')
        quiv2 = ax.quiver(*np.zeros(shape=(3)), *d_norm, color='black')
        scat1 = ax.scatter(*po_intersect)
        plane.show(ax)
        plane.remove_bbox()
        plt.pause(0.1)
        time.sleep(0.2)
        quiv1.remove()
        quiv2.remove()
        scat1.remove()
    plt.show()
def intersection_sphere_and_plane ():
    rng = np.random.Generator(np.random.PCG64(21))
    ax = plt.subplot(projection='3d')
    width = 20
    elev = 1
    azim = -75
    roll = 0
    ax.set_xlim(-width, width); ax.set_ylim(-width, width); ax.set_zlim(-width, width)
    ax.view_init(elev, azim, roll)
    center = np.array([0.63757987,0.96864694,0.75481517])
    pl = plane_stuff.plane.Plane(axes=ax, width=15, center=center) 
    center = np.array([ 1.43509363,6.04270923,-7.14532495])
    s = circle_stuff.circle.Circle(axes=ax, center=center ) 
    n, d = pl.plane_normal()
    
    code = classify_sphere_plane(n, d, s.center, s.r)  # sphere_point_of_contact, sphere_direction or vector direction
    if code != 0:
        d_norm_ = vector3.Vector3(0.78111759 ,0.60584703 ,0.70980119) #rng.random(size=(3)) # direction of sphere
        d_norm = d_norm_.to_numpy()
        # sphere direction will not interact with plane
        if d_norm.dot(n) <= 0.1:
            print('NO INTERSECT')
            return 
        some_sphere = circle_stuff.circle.Circle(axes=ax, center=center )
        poc = s.center - code*s.r*n
        d_dot_n = d_norm.dot(n)
        poc_dot_n = poc.dot(n)
        t = np.divide( d - poc_dot_n, d_dot_n)
        t_mult_d_norm = t*d_norm
        test_pt = poc + t_mult_d_norm
        for i in range(some_sphere.pts.size):
            some_sphere.pts[i].x +=  t_mult_d_norm[0]
            some_sphere.pts[i].y +=  t_mult_d_norm[1]
            some_sphere.pts[i].z +=  t_mult_d_norm[2] 
        some_sphere.show(ax)
        some_sphere.remove_bbox()
        s.show(ax)
        s.remove_bbox()
        pl.show(ax)
        ax.scatter(*test_pt, color='red')
    plt.show()
def classify_sphere_plane(plane_normal, plane_distance, sphere_center, sphere_radius):
    global ax
    # distance from center of sphere to the plane
    d = plane_normal.dot( sphere_center ) - plane_distance
    # completely on front side 
    if d >= sphere_radius:
        print('front')
        ret_code = 1
    # on back side 
    if d <= -sphere_radius:
        print('back')
        return -1
    # in between
    return 0
# Support functions     
def normalize(n: np.ndarray):
    mag = np.linalg.norm(n)
    n_dot_n = mag**2.0
    if np.abs(n_dot_n - 1.0) > 0.01:
        for i in range(n.size):
            n[i] = n[i]/mag
def rotate_pt (n: np.ndarray, deg):
    radians = np.deg2rad(deg)
    cos = np.cos(radians)
    sin = np.sin(radians)
    m = np.array([
        [cos, sin],
        [-sin, cos]
    ])
    return np.matmul(n, m, dtype=np.float32)
def range_interesect_two_ray(p1, p2, d1, d2, id):
    d1_x_d2 = np.cross(d1, d2)
    d1_x_d2_mag = np.linalg.norm(d1_x_d2, ord=2)
    d1_x_d2_mag_sq = np.square(d1_x_d2_mag, dtype=np.float32)
    p_delta = p2 - p1
    def cal_range_id (id):
        if id == 1:
            return np.cross(p_delta, d2).dot(d1_x_d2) / (d1_x_d2_mag_sq)
        elif id == 2:
            return np.cross(p_delta, d1).dot(d1_x_d2) / (d1_x_d2_mag_sq)
    return cal_range_id(id)

if __name__ == '__main__':
    intersection_sphere_and_plane()