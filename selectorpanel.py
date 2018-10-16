from tkinter import StringVar
from tkinter.ttk import Frame, Radiobutton
from enum import Enum

class Layout(Enum):
    DEG_RAD = [
        [('Deg', 'deg'), ('Rad', 'rad')]
    ]

# Container object for a set of related radio buttons. The first button is
# selected by default
class SelectorPanel(Frame):
    def __init__(self, master, layout):
        '''
        Initializes a SelectorPanel object.

        master: a tkinter widget
        layout: a 2D list of tuples. The layout of the list defines the layout
            of the buttons. In each tuple, the first element is a string
            giving the button's text. The second is a string giving the value
            assigned to self.mode when the button is selected.
        
        return: a SelectorPanel object
        '''
        Frame.__init__(self, master)
        self.mode = StringVar()

        for yindex, row in enumerate(layout):
            for xindex, (name, mode) in enumerate(row):
                button = Radiobutton(self, text=name, value=mode, 
                    variable=self.mode)
                button.grid(row=yindex, column=xindex)
                if (xindex, yindex) == (0, 0):
                    button.invoke()
    
    def get_mode(self):
        '''
        Return the value of the button currently selected in the panel.
        '''
        return self.mode.get()

    def set_mode_observer(self, callback):
        self.mode.trace('w', callback)
