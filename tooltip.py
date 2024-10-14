import tkinter
import matplotlib.pyplot as plt 
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter.font import Font

C_FONT_SIZE = 12

class Tooltip():
    def __init__(self, text = "", x = 0,y  = 0, text_scale_factor=1):
        self.mode = 0
        self.text = text
        self.x_mouse = x
        self.y_mouse = y 
        self.frame = tkinter.Frame(relief='groove', borderwidth=20)
        self.frame.columnconfigure(index=0, weight=4)
        self.frame.columnconfigure(index=1, weight=1)
        self.frame.rowconfigure(index=0, weight=1)
        self.frame.rowconfigure(index=1, weight=1)
        self.frame.rowconfigure(index=2, weight=1) 
        self.frame.rowconfigure(index=3, weight=1)
        self.root = tkinter.Toplevel(self.frame)
        self.root.geometry(f'+{x+50 }+{y}')
        self.root.wm_overrideredirect(True)
        self.root.attributes('-alpha', 0.9)
        font_curr = int(C_FONT_SIZE * text_scale_factor)
        tkinter.Label(self.root, text= text, relief='solid', borderwidth = 1, bg='#000000', fg='#ff6700' , font= Font(family='Gigi', size= 1 if font_curr == 0 else font_curr ) ).grid( row= 0 , column = 0  )
        self.root.bind('<Leave>', self.leave)
        self.root.grab_set()
    def leave(self, event=None):
        self.root.destroy()
        del self.root
