import expressionparser as ep
from tkinter import Label

class ExpressionLabel(Label):
    def __init__(self, master, size):
        Label.__init__(self, master, font=('Helvetica', size))
        self.size = size

    def factory(operator):
        
    
    factory = staticmethod(factory)

class FractionLabel(ExpressionLabel):
    def __init__(self, master, size, operation):
        ExpressionLabel.__init__(self, master, size)


    def _show_expression(self, operation):
        numerator = operation.get_first_operand()
        denominator = operation.get_second_operand()

    
    def _create_operand_labels(self, operation):
        num_label = ExpressionLabel.

