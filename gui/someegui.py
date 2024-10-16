import objectv3
import numpy as np 
import tkinter.font
import tkinter as tk 
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter.font import Font
from PIL import Image, ImageTk
import optiongui
import figuregui
import buttongui
import threading
import time 

# C_POLYGON_MENU = ['dots',  'connect_nodes' ,'bbox', 'mesh', 'animate', 'loop']  
# C_POLYGON_MENU_X = 925
# C_POLYGON_MENU_Y =  [ 192, 257, 321 ,385, 450 ,514 ]
C_OPTION_MENU_ITEMS = ['Select Polygon', 'triangle', 'quadrilateral', 'pentagon', 'hexagon', 'heptagon', 'octagon', 'nonagon', 'decagon', 'circle', 'circle3d']
C_PLACEMENT_GRID_N = 15
C_SAMPLES_PER_AXIS = 15
C_PLACEMENT_DICT =dict( width=12, height=2, borderwidth=1.6, relief="groove" )
C_HOLD_DOWN_TIME = 5
class SomeGui():
    """ Have not decided on a clsss for the gui"""
    def __init__(self, title = '', choices=C_OPTION_MENU_ITEMS):
        self.active_obj = None
        self.root = tk.Tk()
        self.root.willdispatch()
        self.root.title(title)
        self.screen_height = self.root.winfo_screenheight()
        self.screen_width = self.root.winfo_screenwidth()
        self.geometry = f'{self.screen_width}x{self.screen_height}'
        self.root.geometry( self.geometry)
        self.hold_counter_start = 0
        self.busy = False
        self.lock = threading.Lock()
        self.x = np.linspace(0, self.screen_width, num=C_PLACEMENT_GRID_N)
        self.y = np.linspace(0, self.screen_height, num=C_PLACEMENT_GRID_N)
        self.delta_x = self.x[1]
        self.delta_y = self.y[1]
        self.x_pl_map = ( self.x * np.ones(shape=C_PLACEMENT_GRID_N)[:, None]).flatten()
        self.y_pl_map =  (self.y[:, None] * np.ones(shape=C_PLACEMENT_GRID_N)).flatten()
        self.place_cells_labeled = False 
        # create placement grid (not tkinter grid library)
        self.placement_grid = np.array([  str for _ in range(int(np.square(C_PLACEMENT_GRID_N)))]).reshape((C_PLACEMENT_GRID_N, C_PLACEMENT_GRID_N)) # alloecate str objects  
        # figure
        self.figure_gui = figuregui.FigureGui(self.root,self.delta_x, self.delta_y)
        # option menu
        self.option_choices = choices
        self.option_gui = optiongui.OptionGui(self.root, self.option_choices, self.delta_x, self.delta_y,  self.figure_gui)
        # button
        self.button_gui = buttongui.ButtonGui(self.root, self.delta_x, self.delta_y, self.figure_gui)
        self.root.bind('<Button>', self.press)
        self.root.bind('<ButtonRelease>', self.release)

    def press(self, e):
        thr = threading.Thread( target=button_press_handler, args=(self, C_HOLD_DOWN_TIME))
        thr.start()
    def release(self, e):
        with self.lock:
            self.busy = False
    def label_cells(self):
        if not self.place_cells_labeled:
            self.place_cells_labeled = True
            self.place_map = [self.topology( int(np.round(  self.y_pl_map [i],2)), int(np.round( self.x_pl_map [i],2)) )  for i in range( self.x_pl_map.size)]
    def run(self):
        self.root.mainloop()
    def event_inject_plt_show(self, *args):
        self.canvas_fig.draw()

    def topology(self, row, col):
        label= tk.Label(self.root, text=f'{col}, {row}', **C_PLACEMENT_DICT)
        label.place( x=col, y=row)        
        return label
    def toggle_place_map(self):
        if hasattr(self, 'place_map'):
            for label in self.place_map:
                label.place_forget() 
            self.place_cells_labeled= False
            del self.place_map

        else:
            self.label_cells() 

def button_press_handler(self, wait_time_sec):
    with  self.lock:
        self.busy = True
        t1 = time.time()
    while True:
        time.sleep(0.5)
        t2 = time.time()
        delta = t2 - t1 
        with self.lock:
            if delta  > wait_time_sec:
                if self.busy:
                    print('show toop tip')
                    label = tk.Label(borderwidth=2 , width=100, height = 100)
                    tooltip = tk.Toplevel(label)
                    self.busy = False
                    tooltip.wm_geometry(  "+%d+%d" % (200, 200)  )
                    tooltip.grid_rowconfigure(index=0, weight=2)
                    tooltip.grid_rowconfigure(index=1, weight=2)
                    button = tk.Button(tooltip, text="show place map", justify='center', relief='solid', borderwidth=1, font=("tahoma", "12", "normal"), width=10, height = 10, command= self.toggle_place_map) 
                    button.grid(row=1, column=0, )
                break
            elif self.busy == False :
                print('realeased early')
                break         

if __name__ == '__main__':
    gui = SomeGui()
    gui.run()
 