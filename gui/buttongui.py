import tkinter as tk 
import os
from PIL import Image, ImageTk
import numpy as np

C_POLYGON_MENU = ['dots.png',  'connect_nodes.png' ,'bbox.png', 'mesh.png', 'animate.png', 'animate.png']  
C_PLACE_X_MIN_INDEX= 9
C_PLACE_Y_MIN_INDEX = 3
C_PLACE_Y_MAX_INDEX = 7
C_PLACE_Y_MIN_HEIGHT_INDEX = 3
C_PLACE_Y_MAX_HEIGHT_INDEX = 9
C_IMAGE_HEIGHT =  50
C_IMAGE_WIDTH = 50

class ButtonGui():
    def __init__(self, root, deltax, deltay, figuregui):
        cwd = os.getcwd()
        self.root = root
        self.container= tk.Frame(self.root)
        self.container.place (x= C_PLACE_X_MIN_INDEX * deltax, y=C_PLACE_Y_MIN_INDEX * deltay ,  height= (C_PLACE_Y_MAX_HEIGHT_INDEX - C_PLACE_Y_MIN_HEIGHT_INDEX)*deltay , width=deltax)
        
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_rowconfigure(0, weight=1) 

        canvas = tk.Canvas(self.container) 
        canvas.grid(row= 0, column = 0, sticky="nsew")
        
        scrollbar = tk.Scrollbar(self.container, orient='vertical', command=canvas.yview)
        scrollbar.grid(row=0,column=9, sticky='ns' )
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas_content_frame = tk.Frame(canvas, borderwidth=1, relief='solid')
        canvas.create_window(0,0, window=canvas_content_frame, anchor='nw')
        canvas_content_frame.bind("<Configure>", lambda event: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas_content_frame.grid_columnconfigure(0, weight=10) 
        canvas_content_frame.grid_rowconfigure(0, weight=1) 

        # add buttons to canvas content frame 
        self.imgs = np.array([ImageTk.PhotoImage for i in range(len(C_POLYGON_MENU))])
        self.frames = np.array([tk.Frame for i in range(len(C_POLYGON_MENU))])
        self.buttons = np.array([tk.Frame for i in range(len(C_POLYGON_MENU))])

        for i, fname in enumerate(C_POLYGON_MENU[:5]):
            path = os.path.join(cwd, 'media', fname)
            img_local = Image.open(path) 
            img = img_local.resize(size=(int(C_IMAGE_WIDTH), int(C_IMAGE_HEIGHT)), resample=Image.Resampling.LANCZOS ) 
            self.imgs[i]  = ImageTk.PhotoImage(img) # reference to imag required
            self.frames[i] = tk.Frame(canvas_content_frame, borderwidth=10, relief='solid', highlightbackground="black", highlightthickness=2, bd=0)
            self.frames[i].grid(row=i, column=0)
            self.frames[i].bind('<Enter>', self.enter_button)
            self.frames[i].bind('<Leave>', self.exit_button)
            
            self.buttons[i]  = tk.Button(self.frames[i]) # set border width to 10 pixels
            self.buttons[i].configure(image=self.imgs[i])
            self.buttons[i].pack()
            self.buttons[i] .index_ = i
            self.buttons[i].bind('<Button>', self.button_pressed)
            self.buttons[i].bind('<ButtonRelease>', self.button_released)
            self.buttons[i].bind('<Button>', figuregui.button_pressed)

    def update_figure(self, deltax, deltay):
        self.delta_x = deltax
        self.delta_y = deltay
        self.container.place (x= C_PLACE_X_MIN_INDEX * deltax, y=C_PLACE_Y_MIN_INDEX * deltay ,  height= (C_PLACE_Y_MAX_HEIGHT_INDEX - C_PLACE_Y_MIN_HEIGHT_INDEX)*deltay , width=deltax)
        
    def button_pressed(self, event: tk.Event):
        w = event.widget.winfo_width()
        h = event.widget.winfo_height()
        py =      (event.widget.index_ + C_PLACE_Y_MIN_INDEX) * self.delta_y
        px =  C_PLACE_X_MIN_INDEX *  self.delta_x 
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
