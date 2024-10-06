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

C_POLYGON_MENU = ['dots',  'connect_nodes' ,'bbox', 'mesh', 'normal', 'loop']  
C_POLYGON_MENU_X = 925
C_POLYGON_MENU_Y =  [ 192, 257, 321 ,385, 450 ,514 ]

class Absolutegui():
    def __init__(self, title = ''):
        self.root = tk.Tk()
        self.root.title(title)
        self.screen_height = self.root.winfo_screenheight()
        self.screen_width = self.root.winfo_screenwidth()
        self.geometry = f'{self.screen_width}x{self.screen_height}'
        self.root.geometry( self.geometry)
        self.figure =  matplotlib.figure.Figure(figsize=(6, 4), dpi=100)
        self.axes = self.figure.add_subplot(projection='3d')
        self.kx = 3
        self.ky = 1
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.columnconfigure(2, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.icons = np.array([tk.Frame for i in range(len(C_POLYGON_MENU))])
        self.label_cells()
        self.add_widgets(0)
        # self.add_widgets(1)
        self.add_widgets(2)
        self.add_widgets(3) 
        self.axes.axis('off')
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
            # self.place_map = [topology(self.root, int(np.round(y[i],2)), int(np.round(x[i],2)) )  for i in range(x.size)]

    def add_widgets(self, type=0):
        if type == 0:
            #canvas frame
            frame = tkinter.Frame(self.root, height=50, width=50)
            frame.place(x=self.delta_x*self.kx, y=192, width= (9 * self.delta_x) - (self.delta_x*self.kx),  height=6*self.delta_y)
            self.canvas = FigureCanvasTkAgg(self.figure, frame)
            self.canvas = self.canvas.get_tk_widget()
            self.canvas.pack(fill='both')
        elif type == 1:
            button_frame = tk.Frame(self.root, borderwidth=2, relief=tk.RIDGE) 
            button_frame.rowconfigure(0, weight=2)
            button_frame.rowconfigure(1, weight=2)

            OPTIONS = ['Select Polygon', 'triangle', 'pentagon']
            dropdown_frame = tk.Frame(button_frame,  borderwidth=3, relief=tk.SOLID)
            dropdown_frame.place(relheight=0.2, relwidth=1, rely=0)
            str_var = tk.StringVar(dropdown_frame,)
            str_var.set(OPTIONS[0])
            dropdown = tk.OptionMenu(dropdown_frame, str_var, *OPTIONS,)
            dropdown.place(relheight=1, relwidth=1, width=4)

            selectable_options_frame = tk.Frame(button_frame,  borderwidth=2, relief=tk.RAISED)
            selectable_options_frame.place(relheight=0.8, relwidth=1, rely=0.2, relx=0)

            scrollable_selectable_options_frame = scrollable_frame(selectable_options_frame)
            scrollable_selectable_options_frame.columnconfigure(index=0, weight=1)
            scrollable_selectable_options_frame.rowconfigure(index=0, weight=1)
            
            button1 = tkinter.Button(scrollable_selectable_options_frame, text=f'Show ', font=Font(family="Arial", size=12), width=10)
            button1.grid(row=0, column=0, columnspan=25)
            button2 = tkinter.Button(scrollable_selectable_options_frame, text=f'Hide', font=Font(family="Arial", size=12), width=10)
            button2.grid(row=1, column=0, columnspan=25)
            button_frame.place(x=925, y=192, width=self.delta_x*3, height=self.delta_y*3)
        elif type == 2:
            dropdown_frame = tkinter.Frame(self.root)
            dropdown_frame.place(x=self.delta_x*self.kx, y=578, width=self.delta_x*6, height=self.delta_y) #set label width|height to pixels         
            OPTIONS = ['Select Polygon', 'triangle', 'pentagon']
            str_var = tk.StringVar(dropdown_frame)
            str_var.set(OPTIONS[0])
            dropdown = tk.OptionMenu(dropdown_frame, str_var, *OPTIONS,)
            dropdown.pack() #(relheight=1, relwidth=1)
        elif type == 3:
            cwd = os.getcwd()
            for i, fname in enumerate(C_POLYGON_MENU):
                path = os.path.join(cwd, 'media', fname + '.png')
                img_local = Image.open(path) 
                img = img_local.resize(size=(int(self.delta_x), int(self.delta_y)), resample=Image.Resampling.LANCZOS ) 
                icon = ImageTk.PhotoImage(img) # ImageTk required for resized images
                frame = tk.Frame(self.root, highlightbackground="black", highlightthickness=2, bd=0)
                frame.place(x=C_POLYGON_MENU_X, y=C_POLYGON_MENU_Y[i], width=self.delta_x, height=self.delta_y)   
                button = tk.Button(frame) # set border width to 10 pixels
                self.icons[i] = button
                button.image = icon
                button.configure(image=icon)
                button.index_ = i
                button.frame_ = frame
                button.place(relheight=1, relwidth=1)
                frame.bind('<Enter>', enter_button)
                frame.bind('<Leave>', exit_button)
                button.bind('<Button>', button_pressed)
                button.bind('<ButtonRelease>', button_released)

    def run(self):
        self.root.mainloop()

def select_op():
    print()
def button_pressed(event: tk.Event):
    w = event.widget.winfo_width()
    h = event.widget.winfo_height()
    py = C_POLYGON_MENU_Y[event.widget.index_]
    px =  C_POLYGON_MENU_X
    if not hasattr(event.widget, 'root_'):
        root = tkinter.Toplevel(event.widget)
        root.overrideredirect(True) # remove minimize/maximize buttons 
        root.attributes('-alpha', 0.3)
        root.geometry(f'{w}x{h}+{px + 7 }+{py + 55}')
        event.widget.root_= root
def button_released(event: tk.Event):
    if hasattr(event.widget, 'root_'):
        event.widget.root_.destroy()
        del event.widget.root_
def enter_button(event: tk.Event):
    event.widget.configure(highlightbackground = 'yellow')
def exit_button(event: tk.Event):
    event.widget.configure(highlightbackground = 'black')

def topology(root, row, col):
    d = dict(borderwidth=1.6, relief="groove")
    width= 12
    label= tk.Label(root, text=f'{col}, {row}', width=width, height=2, font=tkinter.font.Font(family="Arial", size=7) , **d)
    label.place( x=col, y=row)        
    # label.grid( column=col, row=row)
def scrollable_frame(root):
    # create canvas with vertical scrollbar 
    canvas = tk.Canvas(root)
    canvas.place( )
    scrollbar = tk.Scrollbar(root, orient='vertical', command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="right", fill="both")
    scrollbar.pack(side="right", fill="y")
    canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    return scrollable_frame
if __name__ == '__main__':
    gui = Absolutegui()
    gui.run()
 
