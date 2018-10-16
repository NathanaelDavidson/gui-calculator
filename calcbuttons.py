from tkinter import ttk
from tkinter.ttk import Button, Frame, Style
from enum import Enum

class Layouts(Enum):
    TRIG = [
        ['sin'],
        ['cos'], 
        ['tan'],
        ['^'],
        ['e']
    ]

    NUM = [
        ['(', ')', 'BackSpace'],
        [7, 8, 9],
        [4, 5, 6],
        [1, 2, 3],
        ['pi', 0, '.']
    ]

    OPER = [
        ['/'],
        ['*'],
        ['-'],
        ['+'],
        ['=']
    ]


class ButtonPanel(Frame):
    def __init__(self, master, layout, font=('Segoe UI', 14)):
        Frame.__init__(self, master)
        s = ttk.Style()
        s.configure('TButton', font=font)
        self.button_layout = layout.value
        self.buttons = {}
        self.create_buttons()

    def add_button(self, key):
        self.buttons[key] = CalcButton(self, key)

    def bind_all_buttons(self, function):
        for key in self.buttons:
            self.buttons[key].set_callback(function)

    def create_buttons(self):
        num_rows = len(self.button_layout)
        for i in range(num_rows):
            self.create_row(i)

    def create_row(self, row_index):
        num_buttons = len(self.button_layout[row_index])
        next_col_span = 1
        for col_index in range(num_buttons):
            key = self.button_layout[row_index][col_index]
            if key == '':
                next_col_span += 1
            else:
                self.add_button(key)
                self.buttons[key].grid(row=row_index, \
                    column=col_index-next_col_span+1, columnspan=next_col_span, sticky='ew')
                next_col_span = 1

    def get_button_keys(self):
        return self.buttons.keys()
    

class CalcButton(Button):
    def __init__(self, master, key, callback=None):
        Button.__init__(self, master)
        self.key = key
        self.callback = callback
        self.config(command=self.call, text=_get_button_icon(key))

    def call(self):
        self.callback(self.key)

    def set_callback(self, callback):
        self.callback = callback
        self.config(command=self.call)

BUTTON_ICONS = {
    'BackSpace': '\u232b',
    '/': '\u00f7',
    '*': '\u00d7',
    'pi': '\u03c0'
}

def _get_button_icon(key):
    try:
        return BUTTON_ICONS[key]
    except KeyError:
        return key