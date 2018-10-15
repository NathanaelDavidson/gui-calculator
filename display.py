import tkinter as tk

class InputLine(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, background='white')
        self.input_value = tk.StringVar()
        self.result_value = tk.StringVar()

        self.input_view = tk.Entry(self, textvariable=self.input_value, relief='flat')
        self.result_view = tk.Label(self, textvariable=self.result_value, background='white')
        self.show()

    def append_to_input(self, string):
        self.input_view.insert('end', string)

    def backspace(self):
        entry_length = len(self.input_value.get())
        self.input_view.delete(entry_length - 1)

    def clear_input(self):
        self.input_view.delete(0, 'end')

    def set_input_observer(self, callback):
        self.input_value.trace('w', callback)

    def set_result(self, string):
        self.result_value.set(string)

    def get_input(self):
        return self.input_value.get()

    def show(self):
        self.input_view.grid(column=0, row=0, sticky='ew')
        self.result_view.grid(column=1, row=0, sticky='ew')
        self.grid_columnconfigure(0, weight=5)


class HistoryDisplay(tk.Frame):
    def __init__(self, master, entry_callback, rows=4):
        tk.Frame.__init__(self, master)
        self.num_rows = rows
        self.operation_views = [OperationView(self, entry_callback) for i in range(rows)]
        self.show()

    def get_num_rows(self):
        return self.num_rows

    def set_entry(self, row, input_string, result_string):
        self.operation_views[row].set_input_string(input_string)
        self.operation_views[row].set_result_string(result_string)

    def show(self):
        for view in reversed(self.operation_views):
            view.pack()


class OperationView(tk.Frame):
    def __init__(self, master, callback):
        tk.Frame.__init__(self, master)
        self.input_string = ''
        self.result_string = ''
        self.input_view = tk.Button(self, text=self.input_string, 
            relief='flat', borderwidth=0, command=self.call_input)
        self.result_view = tk.Button(self, text=self.result_string, 
            relief='flat', borderwidth=0, command=self.call_result)
        self.callback = callback
        self.show()

    def call_input(self):
        return self.callback(self.input_string)
    
    def call_result(self):
        return self.callback(self.result_string)

    def set_callback(self, callback):
        self.callback = callback

    def set_input_string(self, string):
        self.input_string = string
        self.input_view.config(text=string)

    def set_result_string(self, string):
        self.result_string = string
        self.result_view.config(text='= ' + string)

    def show(self):
        self.input_view.grid(column=0, row=0, columnspan=3, sticky='ew')
        self.result_view.grid(column=3, row=0, sticky='ew')