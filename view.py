from calcbuttons import ButtonPanel, Layouts
from tkinter import ttk
import selectorpanel as sp
from display import InputLine, HistoryDisplay


class View(ttk.Frame):
    def __init__(self):
        ttk.Frame.__init__(self)
        self.input_string = ttk.tkinter.StringVar()
        self.output_string = ttk.tkinter.StringVar()
        self.angle_unit_selector = sp.SelectorPanel(self, sp.Layout.DEG_RAD.value)
        self.button_frame = ttk.Frame(self)
        self.number_panel = ButtonPanel(self.button_frame, Layouts.NUM)
        self.operator_panel = ButtonPanel(self.button_frame, Layouts.OPER)
        self.trig_panel = ButtonPanel(self.button_frame, Layouts.TRIG)
        self.input_line = InputLine(self)
        self.history_display = HistoryDisplay(self, self.set_input_display)
        self.show()
    
    def append_to_input(self, string):
        self.input_line.append_to_input(string)

    def backspace(self):
        self.input_line.backspace()

    def bind_all_buttons(self, func):
        self.number_panel.bind_all_buttons(func)
        self.operator_panel.bind_all_buttons(func)
        self.trig_panel.bind_all_buttons(func)

    def clear_input(self):
        self.input_line.clear_input()

    def get_angle_mode(self):
        return self.angle_unit_selector.get_mode()

    def get_input(self):
        return self.input_line.get_input()

    def set_angle_mode_observer(self, callback):
        return self.angle_unit_selector.set_mode_observer(callback)
    
    def set_current_result(self, string):
        self.input_line.set_result(string)

    def set_history_entry(self, row, input_string, result_string):
        self.history_display.set_entry(row, input_string, result_string)

    def set_input_display(self, text):
        self.input_line.clear_input()
        self.input_line.append_to_input(text)

    def set_input_observer(self, callback):
        self.input_line.set_input_observer(callback)

    def show_button_frame(self):
        self.trig_panel.grid(row=0)
        self.number_panel.grid(row=0, column=1, rowspan=5, columnspan=3)
        self.operator_panel.grid(row=0, column=4, rowspan=5)

        self.button_frame.pack()
    
    def show(self):
        self.grid()
        self.history_display.pack(expand=True, side='top', fill='x')
        self.input_line.pack(expand=True, side='top', fill='x')
        self.angle_unit_selector.pack(expand=True, side='top', fill='x')
        self.show_button_frame()
