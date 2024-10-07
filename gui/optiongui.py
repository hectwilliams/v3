import tkinter as tk 
import objectv3

class OptionGui():
    def __init__(self, parent,  choices  , deltax, deltay, figuregui ):
        dropdown_frame = tk.Frame(parent)
        dropdown_frame.place(x= deltax * 3 , y=578, width=deltax*6, height=deltay) #set label width|height to pixels         
        str_var = tk.StringVar(dropdown_frame)
        str_var.set(choices[0])
        self.dropdown = tk.OptionMenu(dropdown_frame, str_var, *choices, command=figuregui.option_changed)
        self.dropdown.pack()
        self.active_obj = None

