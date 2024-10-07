import numpy as np 
import tkinter.font
import tkinter as tk 
import matplotlib.figure 
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter.font import Font
import os 
from PIL import Image, ImageTk
import time 
import triangle
import quadrilateral
import pentagon
import objectv3
import optiongui
import pprint
import figuregui
import buttongui

C_POLYGON_MENU = ['dots',  'connect_nodes' ,'bbox', 'mesh', 'normal', 'loop']  
C_POLYGON_MENU_X = 925
C_POLYGON_MENU_Y =  [ 192, 257, 321 ,385, 450 ,514 ]
C_OPTION_MENU_ITEMS = ('Select Polygon', 'triangle', 'quadrilateral', 'pentagon')
C_PLACEMENT_GRID_N = 15

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
        
    def label_cells(self):

        C_SAMPLES_PER_AXIS = 15
        if not hasattr(self, 'place_cells_labeled'):
            self.place_cells_labeled = True
            x = np.linspace(0, self.screen_width, num=C_SAMPLES_PER_AXIS)
            y = np.linspace(0, self.screen_height, num=C_SAMPLES_PER_AXIS)
            self.delta_y = y[1]
            self.delta_x = x[1]
            x = x * np.ones(shape=C_SAMPLES_PER_AXIS)[:, None]
            x = x.flatten()
            y = y[:, None] * np.ones(shape=C_SAMPLES_PER_AXIS)
            y = y.flatten()
            self.place_map = [self.topology( int(np.round(y[i],2)), int(np.round(x[i],2)) )  for i in range(x.size)]

            for i in range(225):
                p_row =  int(np.floor(i/15))
                p_col = (i % 15)
                self.placement_grid[p_row][p_col]  = f'({  int(y[i] )  }, { int( x[i])})'

    def run(self):
        self.root.mainloop()
    def event_inject_plt_show(self, *args):
        self.canvas_fig.draw()

    def topology(self, row, col):
        d = dict(borderwidth=1.6, relief="groove")
        width= 12
        label= tk.Label(self.root, text=f'{col}, {row}', width=width, height=2, font=tkinter.font.Font(family="Arial", size=7) , **d)
        label.place( x=col, y=row)        
if __name__ == '__main__':
    gui = SomeGui()
    gui.run()
 
















#     def add_widgets(self, type=0):
#         if type == 0:
#             self.canvas_fig = FigureCanvasTkAgg(self.figure, self.root)
#             self.canvas_fig.get_tk_widget().place(x=self.delta_x*self.kx, y=192, width= (9 * self.delta_x) - (self.delta_x*self.kx),  height=6*self.delta_y)

#         elif type == 1:
#             button_frame = tk.Frame(self.root, borderwidth=2, relief=tk.RIDGE) 
#             button_frame.rowconfigure(0, weight=2)
#             button_frame.rowconfigure(1, weight=2)

#             dropdown_frame = tk.Frame(button_frame,  borderwidth=3, relief=tk.SOLID)
#             dropdown_frame.place(relheight=0.2, relwidth=1, rely=0)
#             str_var = tk.StringVar(dropdown_frame,)
#             str_var.set(C_OPTION_MENU_ITEMS[0])
#             dropdown = tk.OptionMenu(dropdown_frame, str_var, *C_OPTION_MENU_ITEMS,)
#             dropdown.place(relheight=1, relwidth=1, width=4)

#             selectable_options_frame = tk.Frame(button_frame,  borderwidth=2, relief=tk.RAISED)
#             selectable_options_frame.place(relheight=0.8, relwidth=1, rely=0.2, relx=0)

#             scrollable_selectable_options_frame = scrollable_frame(selectable_options_frame)
#             scrollable_selectable_options_frame.columnconfigure(index=0, weight=1)
#             scrollable_selectable_options_frame.rowconfigure(index=0, weight=1)
            
#             button1 = tkinter.Button(scrollable_selectable_options_frame, text=f'Show ', font=Font(family="Arial", size=12), width=10)
#             button1.grid(row=0, column=0, columnspan=25)
#             button2 = tkinter.Button(scrollable_selectable_options_frame, text=f'Hide', font=Font(family="Arial", size=12), width=10)
#             button2.grid(row=1, column=0, columnspan=25)
#             button_frame.place(x=925, y=192, width=self.delta_x*3, height=self.delta_y*3)
#         elif type == 2:
#             dropdown_frame = tkinter.Frame(self.root)
#             dropdown_frame.place(x=self.delta_x*self.kx, y=578, width=self.delta_x*6, height=self.delta_y) #set label width|height to pixels         
#             str_var = tk.StringVar(dropdown_frame)
#             str_var.set(C_OPTION_MENU_ITEMS[0])
#             dropdown = tk.OptionMenu(dropdown_frame, str_var, *C_OPTION_MENU_ITEMS, command=self.option_changed)
#             dropdown.pack() #(relheight=1, relwidth=1)
#         elif type == 3:
#             cwd = os.getcwd()
#             for i, fname in enumerate(C_POLYGON_MENU):
#                 path = os.path.join(cwd, 'media', fname + '.png')
#                 img_local = Image.open(path) 
#                 img = img_local.resize(size=(int(self.delta_x), int(self.delta_y)), resample=Image.Resampling.LANCZOS ) 
#                 icon = ImageTk.PhotoImage(img) # ImageTk required for resized images
#                 frame = tk.Frame(self.root, highlightbackground="black", highlightthickness=2, bd=0)
#                 frame.place(x=C_POLYGON_MENU_X, y=C_POLYGON_MENU_Y[i], width=self.delta_x, height=self.delta_y)   
#                 button = tk.Button(frame) # set border width to 10 pixels
#                 self.icons[i] = button
#                 button.configure(image=icon)
#                 button.index_ = i
#                 button.frame_ = frame
#                 button.place(relheight=1, relwidth=1)
#                 frame.bind('<Enter>', enter_button)
#                 frame.bind('<Leave>', exit_button)
#                 button.bind('<Button>', button_pressed)
#                 button.bind('<ButtonRelease>', button_released)
#     def option_changed(self, str):
#         if not self.active_obj:
#             # TODO clean up 
#             pass 
#         obj = objectv3.Objectv3()
#         if str == 'triangle':
#             obj = triangle.Triangle(self.axes)
#         elif str == 'quadrilateral':
#             obj = quadrilateral.Quadrilateral(self.axes)
#         elif str == 'pentagon':
#             obj = pentagon.Pentagon(self.axes)
#         self.axes.clear()
#         self.axes.axis('off')
#         obj.show()
#         obj.remove_bbox()
#         obj.connect_vertices_plot(c='black')
#         self.root.event_generate('<<Plt_Update>>', when='tail')



# def button_pressed(event: tk.Event):
#     w = event.widget.winfo_width()
#     h = event.widget.winfo_height()
#     py = C_POLYGON_MENU_Y[event.widget.index_]
#     px =  C_POLYGON_MENU_X
#     if not hasattr(event.widget, 'root_'):
#         root = tkinter.Toplevel(event.widget)
#         root.overrideredirect(True) # remove minimize/maximize buttons 
#         root.attributes('-alpha', 0.3)
#         root.geometry(f'{w}x{h}+{px + 7 }+{py + 55}')
#         event.widget.root_= root
# def button_released(event: tk.Event):
#     if hasattr(event.widget, 'root_'):
#         event.widget.root_.destroy()
#         del event.widget.root_
# def enter_button(event: tk.Event):
#     event.widget.configure(highlightbackground = 'yellow')
# def exit_button(event: tk.Event):
#     event.widget.configure(highlightbackground = 'black')

# def scrollable_frame(root):
#     # create canvas with vertical scrollbar 
#     c = tk.Canvas(root)
#     c.place( )
#     scrollbar = tk.Scrollbar(root, orient='vertical', command=c.yview)
#     scrollable_frame = tk.Frame(c)
#     c.create_window((0, 0), window=scrollable_frame, anchor="nw")
#     c.configure(yscrollcommand=scrollbar.set)
#     c.pack(side="right", fill="both")
#     scrollbar.pack(side="right", fill="y")
#     c.bind("<Configure>", lambda e: c.configure(scrollregion=c.bbox("all")))
#     return scrollable_frame
