import objectv3 
import tkinter as tk 
import matplotlib.pyplot as plt 
import matplotlib.figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import triangle, quadrilateral, pentagon, hexagon, heptagon, octagon, nonagon, decagon, circle
import threading
import quarternion
import numpy as np 
import time 
import tooltip
C_PLACE_HEIGHT_STEP_MAX = 6
C_PLACE_HEIGHT_STEP_MIN = 3
C_PLACE_WIDTH_STEP_MAX = 9
C_PLACE_WIDTH_STEP_MIN = 3

class FigureGui():
    def __init__(self, root, deltax, deltay):
        self.figure = matplotlib.figure.Figure(figsize=(6, 4), dpi=100) # (w, h) inches * 100 dpi (dots per inch)
        self.axes = self.figure.add_subplot(projection='3d')
        self.root = root 
        self.frame = tk.Frame(self.root)
        self.canvas_fig = FigureCanvasTkAgg(self.figure, self.frame)
        self.canvas_fig.get_tk_widget().place(relheight=1, relwidth=1)
        self.frame.place(x=deltax*C_PLACE_WIDTH_STEP_MIN, y=deltay*C_PLACE_HEIGHT_STEP_MIN, width= (C_PLACE_WIDTH_STEP_MAX * deltax) - (deltax*C_PLACE_WIDTH_STEP_MIN),  height=C_PLACE_HEIGHT_STEP_MAX*deltay)
        self.frame.lift()
        self.frame.lift()
        self.axes.axis('off')
        self.lock = threading.Lock() 
        self.active_obj = None
        self.root.bind('<Motion>', self.motion )
        self.mouse_pos = dict(x=0, y=0)
    def update_figure(self, deltax, deltay):
        self.frame.place(x=deltax*C_PLACE_WIDTH_STEP_MIN, y=deltay*C_PLACE_HEIGHT_STEP_MIN, width= (C_PLACE_WIDTH_STEP_MAX * deltax) - (deltax*C_PLACE_WIDTH_STEP_MIN),  height=C_PLACE_HEIGHT_STEP_MAX*deltay)
    def motion(self, event:tk.Event):
        self.mouse_pos['x'] = event.x_root
        self.mouse_pos['y'] = event.y_root
    def option_changed(self, str):
        if str == 'triangle':
            self.active_obj = triangle.Triangle(self.axes)
        elif str == 'quadrilateral':
            self.active_obj = quadrilateral.Quadrilateral(self.axes)
        elif str == 'pentagon':
            self.active_obj = pentagon.Pentagon(self.axes)
        elif str == 'hexagon':
            self.active_obj = hexagon.Hexagon(self.axes)
        elif str == 'heptagon':
            self.active_obj = heptagon.Heptagon(self.axes)
        elif str == 'octagon':
            self.active_obj = octagon.Octagon(self.axes)
        elif str == 'nonagon':
            self.active_obj = nonagon.Nonagon(self.axes)
        elif str == 'decagon':
            self.active_obj = decagon.Decagon(self.axes)
        elif str == 'circle':
            self.active_obj = circle.Circle(self.axes)
        elif str == 'circle3d':
            self.active_obj = circle.Circle(self.axes, use_mesh_grid=True)
        else:
            self.active_obj = None
        if self.active_obj:
            self.repaint_canvas() 
    def button_pressed(self, event: tk.Event):
        if not self.active_obj:
            raise RuntimeWarning('Not image on canvas')
        
        if  hasattr(self, 'tooltopbox') and hasattr(self.tooltopbox, 'root'):
            raise RuntimeWarning('tooltip not exited')
        
        if event.widget.index_ != 4 and hasattr(self, 'aninmation_on'):
            msg = 'please stop animation, before selection'
            thr = threading.Thread(target=animate_warning, args=(self, msg, self.mouse_pos['x'], self.mouse_pos['y'] ))
            thr.start()
            del self.aninmation_on
            return 

        if event.widget.index_ == 0:
            self.active_obj.toggle_vertices()
            self.canvas_fig.draw()
        elif event.widget.index_ == 1:
            self.active_obj.toggle_connect_line()
            self.canvas_fig.draw()
        elif event.widget.index_ == 2:
            self.active_obj.toggle_bbox()
            self.canvas_fig.draw()
        elif event.widget.index_ == 3:
            self.active_obj.toggle_mesh()
            self.canvas_fig.draw()
        elif event.widget.index_ == 4:
            if not hasattr(self, 'aninmation_on'):
                self.aninmation_on = True
                thr = threading.Thread( target=rotate_about_z_axis, args= (self, self.lock,) )
                thr.start()
            else:
                self.aninmation_on = not self.aninmation_on

    def repaint_canvas(self):
        self.axes.clear()
        self.axes.axis('off')
        self.active_obj.show(hide_bbox=True , s=1)
        self.active_obj.remove_bbox()
        self.canvas_fig.draw()

def animate_warning(figure_gui,  msg, x, y):
    figure_gui.tooltopbox = tooltip.Tooltip(text=msg, x= x , y = y )
    t0 = time.time() 
    while True:
        elaspsed_time = time.time() - t0
        if elaspsed_time > 2:
            figure_gui.tooltopbox.root.event_generate('<Leave>') 
            break
    del figure_gui.tooltopbox 

#TODO rotation does not following contour on z place 
def rotate_about_z_axis(figure_gui, lock ):
    deg = 1
    q = quarternion.Quarternion()
    q.set_to_rotate_about_z(np.deg2rad(deg))
    while True:
        if not hasattr(figure_gui, 'aninmation_on'):
            break
        elif figure_gui.aninmation_on:
            figure_gui.active_obj.xform_q(q)
            figure_gui.repaint_canvas()
        time.sleep(0.01)