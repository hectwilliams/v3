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
class FigureGui():
    def __init__(self, root, deltax, deltay):
        self.figure = matplotlib.figure.Figure(figsize=(6, 4), dpi=100) # (w, h) inches * 100 dpi (dots per inch)
        self.axes = self.figure.add_subplot(projection='3d')
        self.root = root 
        self.frame = tk.Frame(self.root)
        self.canvas_fig = FigureCanvasTkAgg(self.figure, self.frame)
        self.canvas_fig.get_tk_widget().place(relheight=1, relwidth=1)
        self.frame.place(x=deltax*3, y=192, width= (9 * deltax) - (deltax*3),  height=6*deltay)
        self.frame.lift()
        self.frame.lift()
        self.axes.axis('off')
        self.lock = threading.Lock() 
        self.active_obj = None
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
        if event.widget.index_ != 4 and hasattr(self, 'aninmation_on'):
            if self.lock.locked():
                print('DAMNNt')
            with self.lock:
                del self.aninmation_on
            time.sleep(0.0)

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

def rotate_about_z_axis(figure_gui, lock ):
    deg = 1
    q = quarternion.Quarternion()
    q.set_to_rotate_about_z(np.deg2rad(deg))
    while True:
        with lock:
            if not hasattr(figure_gui, 'aninmation_on'):
                break
            elif figure_gui.aninmation_on:
                figure_gui.active_obj.xform_q(q)
                # figure_gui.active_obj.sequencer()
                figure_gui.repaint_canvas()
        time.sleep(0.1)