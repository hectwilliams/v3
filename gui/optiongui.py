import tkinter as tk 

C_PLACE_X_POS_MULT_FACTOR= 3
C_PLACE_Y_POS_MULT_FACTOR= 9
C_PLACE_WIDTH_MULT_FACTOR= 6
C_PLACE_HEIGHT_MULT_FACTOR= 3

class OptionGui():
    def __init__(self, parent,  choices  , deltax, deltay, figuregui ):
        self.dropdown_frame = tk.Frame(parent)
        self.dropdown_frame.place(x= deltax * C_PLACE_X_POS_MULT_FACTOR , y=deltay*C_PLACE_Y_POS_MULT_FACTOR, width=deltax*C_PLACE_WIDTH_MULT_FACTOR, height=deltay) #set label width|height to pixels         
        str_var = tk.StringVar( self.dropdown_frame )
        str_var.set(choices[0])
        self.dropdown = tk.OptionMenu( self.dropdown_frame , str_var, *choices, command=figuregui.option_changed)
        self.dropdown.pack()
        self.active_obj = None
    def update_figure(self, deltax, deltay):
        self.dropdown_frame.place(x= deltax * C_PLACE_X_POS_MULT_FACTOR , y=deltay*C_PLACE_Y_POS_MULT_FACTOR, width=deltax*C_PLACE_WIDTH_MULT_FACTOR, height=deltay) #set label width|height to pixels         