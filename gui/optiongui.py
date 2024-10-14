import tkinter as tk 

C_PLACE_X_POS_MULT_FACTOR= 3
C_PLACE_Y_POS_MULT_FACTOR= 9
C_PLACE_WIDTH_MULT_FACTOR= 6
C_PLACE_HEIGHT_MULT_FACTOR= 3

class OptionGui():
    def __init__(self, parent,  choices  , deltax, deltay, figuregui ):
        self.dropdown_frame = tk.Frame(parent,pady=4, bg='black')
        self.dropdown_frame.place(x= deltax * C_PLACE_X_POS_MULT_FACTOR , y=deltay*C_PLACE_Y_POS_MULT_FACTOR, width=deltax*C_PLACE_WIDTH_MULT_FACTOR, height=deltay, ) #set label width|height to pixels         
        label_frame = tk.LabelFrame(master=self.dropdown_frame, borderwidth=2, relief='solid' )
        label_frame.place(relx=0.5, y=0.5)
        str_var = tk.StringVar( label_frame  )
        str_var.set(choices[0])
        self.dropdown = tk.OptionMenu( self.dropdown_frame , str_var, *choices, command=figuregui.option_changed, )
        self.dropdown.place(x=0, y=0)
        self.active_obj = None
    def update_figure(self, deltax, deltay):
        self.dropdown_frame.place(x= deltax * C_PLACE_X_POS_MULT_FACTOR , y=deltay*C_PLACE_Y_POS_MULT_FACTOR, width=deltax*C_PLACE_WIDTH_MULT_FACTOR, height=deltay * 2) #set label width|height to pixels         
        self.dropdown.place(x=0, y=0)