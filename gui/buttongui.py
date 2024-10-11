import tkinter as tk 
import objectv3
import triangle, quadrilateral, pentagon
import os
from PIL import Image, ImageTk
import numpy as np

C_POLYGON_MENU = ['dots.png',  'connect_nodes.png' ,'bbox.png', 'mesh.png', 'animate.png', 'animate.png']  
C_POLYGON_MENU_X = 925
C_POLYGON_MENU_Y =  [ 192, 257, 321 ,385, 450 ,514 ]

class ButtonGui():
    def __init__(self, root, deltax, deltay, figuregui):
        cwd = os.getcwd()
        self.root = root
        self.imgs = np.array([ImageTk.PhotoImage for i in range(len(C_POLYGON_MENU))])
        self.frames = np.array([tk.Frame for i in range(len(C_POLYGON_MENU))])
        self.buttons = np.array([tk.Frame for i in range(len(C_POLYGON_MENU))])

        for i, fname in enumerate(C_POLYGON_MENU[:5]):
            path = os.path.join(cwd, 'media', fname)
            img_local = Image.open(path) 
            img = img_local.resize(size=(int(deltax), int(deltay)), resample=Image.Resampling.LANCZOS ) 
            self.imgs[i]  = ImageTk.PhotoImage(img) # reference to imag required
            
            self.frames[i]  = tk.Frame(self.root, highlightbackground="black", highlightthickness=2, bd=0)
            self.frames[i].place(x=C_POLYGON_MENU_X, y=C_POLYGON_MENU_Y[i], width=deltax, height=deltay)   
            self.frames[i].bind('<Enter>', self.enter_button)
            self.frames[i].bind('<Leave>', self.exit_button)
            
            self.buttons[i]  = tk.Button(self.frames[i]) # set border width to 10 pixels
            self.buttons[i].configure(image=self.imgs[i])
            self.buttons[i].place(relheight=1, relwidth=1)
            self.buttons[i] .index_ = i
            self.buttons[i].bind('<Button>', self.button_pressed)
            self.buttons[i].bind('<ButtonRelease>', self.button_released)
            self.buttons[i].bind('<Button>', figuregui.button_pressed)

    def button_pressed(self, event: tk.Event):
        w = event.widget.winfo_width()
        h = event.widget.winfo_height()
        py = C_POLYGON_MENU_Y[event.widget.index_]
        px =  C_POLYGON_MENU_X
        if not hasattr(event.widget, 'root_'):
            root = tk.Toplevel(event.widget)
            root.overrideredirect(True) # remove minimize/maximize buttons 
            root.attributes('-alpha', 0.3)
            root.geometry(f'{w}x{h}+{px + 7 }+{py + 55}')
            event.widget.root_= root
    def button_released(self, event: tk.Event):
        if hasattr(event.widget, 'root_'):
            event.widget.root_.destroy()
            del event.widget.root_
    def enter_button(self, event: tk.Event):
        event.widget.configure(highlightbackground = 'yellow')
    def exit_button(self, event: tk.Event):
        event.widget.configure(highlightbackground = 'black')