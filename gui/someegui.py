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

C_POLYGON_MENU = ['dots',  'connect_nodes' ,'bbox', 'mesh', 'normal', 'loop']  
C_POLYGON_MENU_X = 925
C_POLYGON_MENU_Y =  [ 192, 257, 321 ,385, 450 ,514 ]
C_OPTION_MENU_ITEMS = ['Select Polygon', 'triangle', 'quadrilateral', 'pentagon', 'hexagon', 'heptagon', 'octagon', 'nonagon', 'decagon', 'circle', 'circle3d']
C_PLACEMENT_GRID_N = 15
C_SAMPLES_PER_AXIS = 15

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
        # create placement grid (not tkinter grid library)
        self.placement_grid = np.array([  str for _ in range(int(np.square(C_PLACEMENT_GRID_N)))]).reshape((C_PLACEMENT_GRID_N, C_PLACEMENT_GRID_N)) # alloecate str objects  
        self.label_cells()
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
        thr = threading.Thread( target=button_press_handler, args=(self, 3))
        thr.start()
    def release(self, e):
        with self.lock:
            self.busy = False
    def label_cells(self):
        if not hasattr(self, 'place_cells_labeled'):
            self.place_cells_labeled = True
            x = np.linspace(0, self.screen_width, num=C_PLACEMENT_GRID_N)
            y = np.linspace(0, self.screen_height, num=C_PLACEMENT_GRID_N)
            self.delta_y = y[1]
            self.delta_x = x[1]
            x = x * np.ones(shape=C_PLACEMENT_GRID_N)[:, None]
            x = x.flatten()
            y = y[:, None] * np.ones(shape=C_PLACEMENT_GRID_N)
            y = y.flatten()
            self.place_map = [self.topology( int(np.round(y[i],2)), int(np.round(x[i],2)) )  for i in range(x.size)]
            # for i in range(int(C_PLACEMENT_GRID_N**2)):
            #     p_row =  int(np.floor(i/C_PLACEMENT_GRID_N))
            #     p_col = (i % C_PLACEMENT_GRID_N)
            #     self.placement_grid[p_row][p_col]  = f'({  int(y[i] )  }, { int( x[i])})'
    def run(self):
        self.root.mainloop()
    def event_inject_plt_show(self, *args):
        self.canvas_fig.draw()

    def topology(self, row, col):
        label= tk.Label(self.root, text=f'{col}, {row}', width=12, height=2, font=tkinter.font.Font(family="Arial", size=7) , borderwidth=1.6, relief="groove" )
        label.place( x=col, y=row)        
        return label
    def toggle_place_map(self):
        if hasattr(self, 'place_map'):
            for label in self.place_map:
                label.place_forget() 
            del self.place_map
            del self.place_cells_labeled  
        else:
            self.label_cells() 
            print('relabel')

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
 