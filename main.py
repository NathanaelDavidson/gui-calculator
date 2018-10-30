import tkinter as tk
import expressionparser as ep
import view


class Controller:
    def __init__(self):
        self.model = Model()
        self.view = view.View()

        self.button_functions = {
            '=': self.execute_operation,
            'BackSpace': self.backspace
        }

        self._set_bindings()
        self.view.set_angle_mode_observer(self.update_angle_mode)
        self.view.set_input_observer(self.update_operation)
        self.update_angle_mode()

    def add_entry(self, entry):
        self.view.append_to_input(entry)

    def backspace(self, args=None):
        self.view.backspace()

    def clear_input_display(self, *args):
        self.view.clear_input()
        self.view.set_current_result('')

    def execute_operation(self, args=None):
        try:
            self.model.get_result()
        except ZeroDivisionError:
            pass
        except ep.MathSyntaxError:
            self.view.set_current_result('SYNTAX ERROR')
        else:        
            self.model.push_operation_to_history()
            self._update_history_display()
            self.clear_input_display()

    def update_operation(self, *args):
        expression = self.view.get_input()
        self.model.set_operation_from_expression(expression)
        try:
            self.view.set_current_result('= ' + str(self.model.get_result()))
        except ZeroDivisionError:
            self.view.set_current_result('DIV/0 ERROR')
        except ep.MathSyntaxError:
            self.view.set_current_result('')

    def set_input_display(self, text):
        self.view.set_input_display(text)

    def update_angle_mode(self, *args):
        mode = self.view.get_angle_mode()
        self.model.set_angle_mode(mode)

    def _handle_button_input(self, key):
        try:
            return self.button_functions[key]()
        except KeyError:
            return self.add_entry(key)

    def _handle_keyboard_input(self, event):
        if len(event.char) > 0:
            key = event.char
        else:
            key = event.keysym
        return self._handle_button_input(key)

    def _set_bindings(self):
        self._set_button_bindings()
        self._set_key_bindings()

    def _set_button_bindings(self):
        self.view.bind_all_buttons(self._handle_button_input)
    
    def _set_key_bindings(self):
        self.view.bind('<BackSpace>', self.backspace)
        self.view.bind('<Return>', self.execute_operation)

    def _update_history_display(self):
        history = self.model.get_history()
        history_length = len(history)
        for i in range(history_length):
            operation = history[i]
            input_string = str(operation)
            result_string = str(operation.get_value())
            try:
                self.view.set_history_entry(i, input_string, result_string)
            except IndexError:
                break


class Model:
    HIST_SIZE = 100
    ANGLE_MODES = {
        'deg': True,
        'rad': False
    }

    def __init__(self):
        self.history = []
        self.current_operation = None
        self.parser = ep.Parser()

    def get_current_operation(self):
        return self.current_operation
    
    def get_history(self):
        return self.history

    def push_operation_to_history(self):
        print('pushing %s to history' % str(self.current_operation))
        while len(self.history) >= Model.HIST_SIZE:
            self.history.pop()
        self.history.insert(0, self.current_operation)
        self.current_operation = None

    def set_angle_mode(self, mode):
        use_degrees = Model.ANGLE_MODES[mode]
        self.parser.set_use_degrees(use_degrees)

    def set_operation_from_expression(self, expression):
        self.current_operation = self.parser.parse_exp(expression)

    def get_result(self):
        return self.current_operation.get_value()

        
if __name__ == '__main__':
    root = tk.Tk()
    root.title('Calculator')
    root.iconbitmap('icons/Dtafalonso-Calculator.ico')
    root.option_add('*Font', ('Segoe UI', 14))
    app = Controller()
    root.mainloop()