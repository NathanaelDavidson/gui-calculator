import math
import trigconfig as tc


class Parser:
    INFIX_OPERATORS = {
        '+': {'prec': 0, 'func': lambda a, b: a + b},
        '-': {'prec': 0, 'func': lambda a, b: a - b},
        '*': {'prec': 1, 'func': lambda a, b: a * b},
        '/': {'prec': 1, 'func': lambda a, b: a / b},
        '^': {'prec': 2, 'func': lambda a, b: a ** b}
    }
    POSTFIX_OPERATORS = {
        '!': {'prec': 3, 'func': math.factorial}
    }
    FUNCTION_PRECEDENCE = 1000

    def __init__(self, use_degrees=False):
        self.trig_config = tc.TrigConfigurator(use_degrees)
        self.functions = {
            'sin': self.trig_config.sin,
            'cos': self.trig_config.cos,
            'tan': self.trig_config.tan
        }
        self.current_item = None
        self.parent_stack = []
        self.input_buffer = _InputBuffer()

    def append_to_operation(self, char):
        if self._is_infix_operator(char):
            self._empty_input_buffer()
            if not self.current_item:
                if char == '-':
                    new_operator = Operator('-', lambda a: -1 * a, Parser.FUNCTION_PRECEDENCE)
                    self.parent_stack.append(Function(new_operator))
                else:
                    raise MathSyntaxError
            else:
                self._insert_new_infix_operation(char)
        elif self._is_postfix_operator(char):
            self._empty_input_buffer()
            self._insert_new_postfix_operation(char)
        elif char == '(':
            self._empty_input_buffer()
            self.parent_stack.append(self.current_item)
            self.current_item = None
        elif char == ')':
            self._empty_input_buffer()
            try:
                self._move_to_parent()
            except ParentNotFoundError:
                raise MathSyntaxError
        else:
            self.input_buffer.insert(char)

    def parse_exp(self, expression):
        """
        Parses a valid mathematical expression into an Operation object for
        evaluation. Operations are structured like a tree, where each operand
        may also be an operation.

        expression: string containing a valid mathematical expression using
            infix notation
        """

        self.current_item = None
        self.parent_stack = []
        self.input_buffer.reset()

        for char in expression:
            self.append_to_operation(char)
        self._empty_input_buffer()

        while len(self.parent_stack):
            self._move_to_parent()

        return self.current_item

    def set_use_degrees(self, use_degrees):
        self.trig_config.set_mode(use_degrees)

    def _empty_input_buffer(self):
        if not self.input_buffer.is_empty:
            input_val = self.input_buffer.get_input_and_clear()
            if isinstance(input_val, float) or isinstance(input_val, int):
                self._insert_new_operand(Operand(input_val))
            elif isinstance(input_val, str):
                if input_val in self.functions.keys():
                    self._insert_new_function(input_val)
                elif input_val in Constant.VALUES.keys():
                    self._insert_new_operand(Constant(input_val))

    def _insert_new_function(self, symbol):
        if self.current_item:
            raise MathSyntaxError
        else:
            new_operator = self._make_function(symbol)
            new_operation = Function(new_operator)
            self.parent_stack.append(new_operation)

    def _insert_new_infix_operation(self, symbol):
        operator = self._make_infix_operator(symbol)
        while self._parent_has_precedence_over(operator):
            self._move_to_parent()
        new_operation = BinaryOperation(operator, self.current_item)
        self.parent_stack.append(new_operation)
        self.current_item = None

    def _insert_new_postfix_operation(self, symbol):
        operator = self._make_postfix_operator(symbol)
        while self._parent_has_precedence_over(operator):
            self._move_to_parent()
        new_operation = UnaryOperation(operator, self.current_item)
        self.current_item = new_operation

    def _insert_new_operand(self, operand):
        try:
            self.current_item.insert_operand(operand)
        except AttributeError:
            if not self.current_item:
                self.current_item = operand
            else:
                raise MathSyntaxError

    def _is_infix_operator(self, char):
        return char in Parser.INFIX_OPERATORS

    def _is_postfix_operator(self, char):
        return char in Parser.POSTFIX_OPERATORS

    def _make_postfix_operator(self, symbol):
        func = Parser.POSTFIX_OPERATORS[symbol]['func']
        precedence = Parser.POSTFIX_OPERATORS[symbol]['prec']
        return Operator(symbol, func, precedence)

    def _make_infix_operator(self, symbol):
        func = Parser.INFIX_OPERATORS[symbol]['func']
        precedence = Parser.INFIX_OPERATORS[symbol]['prec']
        return Operator(symbol, func, precedence)

    def _make_function(self, symbol):
        func = self.functions[symbol]
        return Operator(symbol, func, Parser.FUNCTION_PRECEDENCE)

    def _move_to_parent(self):
        current_operation = self.current_item
        try:
            self.current_item = self.parent_stack.pop()
        except IndexError:
            raise ParentNotFoundError
        else:
            self._insert_new_operand(current_operation)

    def _parent_has_precedence_over(self, operator):
        try:
            parent = self.parent_stack[-1]
        except IndexError:
            return False
        else:
            return parent and parent.get_precedence() > operator.get_precedence()

    def _print_parent_stack(self):
        string = '[%s]' % ', '.join([str(item) for item in self.parent_stack])
        print(string)


class Operand(object):
    def __init__(self, value, alias=None):
        """
        Initializes an Operand object.

        value: int or float giving the operand's value
        alias: desired string representation for the operand. If
            defined, overrides the default return value for self.__str__().
        """
        self.value = value
        self.alias = alias

    def get_value(self):
        return self.value

    def set_value(self, value):
        self.value = value

    # For desired behavior, do not override this method in subclasses.
    # To define default string representation, instead override the 
    # _calc_string() method.
    def __str__(self):
        if self.alias:
            return self.alias
        else:
            return self._calc_string()

    def _calc_string(self):
        return str(self.value)


class Constant(Operand):
    VALUES = {
        'pi': math.pi,
        'e': math.e
    }

    UNICODE_SYMBOLS = {
        'pi': '\ucf80',
        'e': '\U0001D452'
    }

    def __init__(self, key):
        Operand.__init__(self, Constant.VALUES[key])
        self.key = key

    def _calc_string(self):
        return self.key

    def get_unicode_exp(self):
        return Constant.UNICODE_SYMBOLS[self.key]


class Operation(Operand):
    def __init__(self, operator):
        Operand.__init__(self, None)
        self.operator = operator

    def get_operator(self):
        return self.operator

    def get_precedence(self):
        return self.operator.get_precedence()

    def get_value(self):
        self._evaluate()
        return self.value

    def get_last_operand(self):
        raise NotImplementedError

    def insert_operand(self, operand):
        raise NotImplementedError

    def _evaluate(self):
        raise NotImplementedError


class BinaryOperation(Operation):
    def __init__(self, operator, first_operand):
        Operation.__init__(self, operator)
        self.first_operand = first_operand
        self.second_operand = None

    def get_first_operand(self):
        return self.first_operand

    def get_last_operand(self):
        return self.second_operand

    def insert_operand(self, operand):
        if not self.first_operand:
            self.first_operand = operand
        elif not self.second_operand:
            self.second_operand = operand
        else:
            raise UnexpectedOperandError

    def set_second_operand(self, operand):
        self.second_operand = operand

    def _evaluate(self):
        try:
            first_operand_val = self.first_operand.get_value()
            second_operand_val = self.second_operand.get_value()
        except AttributeError:
            raise MathSyntaxError
        else:
            func = self.operator.get_function()
            self.value = func(first_operand_val, second_operand_val)

    def _calc_string(self):
        string_rep = ''
        if isinstance(self.first_operand, Operation) and \
                self.get_precedence() > self.first_operand.get_precedence():
            string_rep += '(%s)' % str(self.first_operand)
        else:
            string_rep += str(self.first_operand)

        string_rep += str(self.operator)

        if isinstance(self.second_operand, Operation) and \
                self.get_precedence() > self.second_operand.get_precedence():
            string_rep += '(%s)' % str(self.second_operand)
        else:
            string_rep += str(self.second_operand)

        return string_rep


class UnaryOperation(Operation):
    def __init__(self, operator, operand=None):
        Operation.__init__(self, operator)
        self.operand = operand

    def get_last_operand(self):
        return self.operand

    def insert_operand(self, operand):
        if not self.operand:
            self.operand = operand
        else:
            raise UnexpectedOperandError

    def _evaluate(self):
        operand_val = self.operand.get_value()
        func = self.operator.get_function()
        self.value = func(operand_val)

    def _calc_string(self):
        if isinstance(self.operand, Operation) and \
                self.get_precedence() > self.operand.get_precedence():
            return '(%s)%s' % (str(self.operand), str(self.operator))
        else:
            return '%s%s' % (str(self.operand), str(self.operator))


class Function(UnaryOperation):
    def __init__(self, operator):
        UnaryOperation.__init__(self, operator)

    def _calc_string(self):
        return '%s(%s)' % (str(self.operator), str(self.operand))


class Operator:
    def __init__(self, symbol, func, precedence):
        self.symbol = symbol
        self.function = func
        self.precedence = precedence

    def get_function(self):
        return self.function

    def get_precedence(self):
        return self.precedence

    def __str__(self):
        return self.symbol


class _InputBuffer:
    def __init__(self):
        self.data = []
        self.input_type = None

    def get_input_and_clear(self):
        result = self.input_type(''.join(self.data))
        self.reset()
        print('result:' + str(result))
        return result

    def insert(self, char):
        if not self.input_type:
            self._choose_input_type(char)
        elif self.input_type == int:
            if char == '.' or char.lower() == 'e' and 'e' not in [c.lower() for c in self.data]:
                self.input_type = float
            elif not char.isdecimal():
                raise MathSyntaxError('Unexpected character ' + char)
        elif self.input_type == float:
            if not (char.isdecimal() or char.lower() == 'e' and 'e' not in [c.lower() for c in self.data]):
                raise MathSyntaxError('Unexpected character ' + char)
        elif self.input_type == str:
            if not char.isalpha():
                raise MathSyntaxError('Unexpected character ' + char)
        self.data.append(char)
        for item in self.data:
            print(item, end=',')
        print()

    @property
    def is_empty(self):
        return not bool(len(self.data))

    def reset(self):
        self.data = []
        self.input_type = None

    def _choose_input_type(self, first_char):
        # Sets self.input_type to the appropriate type based on the first character to be stored in the buffer
        if first_char.isdecimal():
            self.input_type = int
        elif first_char.isalpha():
            self.input_type = str
        elif first_char == '.':
            self.input_type = float
        else:
            raise MathSyntaxError('Unexpected character ' + first_char)


class MathSyntaxError(Exception):
    pass


class ParentNotFoundError(Exception):
    pass


class UnexpectedOperandError(Exception):
    pass
