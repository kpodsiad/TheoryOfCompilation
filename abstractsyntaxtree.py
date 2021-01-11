from abc import ABCMeta
import numpy as np
import operator
from Exceptions import ReturnValueException


def multiply(first, second):
    if type(first) == type(second) == np.ndarray:
        return first @ second
    else:
        return first * second


operators = {
    '==': operator.eq, '!=': operator.ne,
    '>': operator.gt, '<': operator.lt,
    '>=': operator.ge, '<=': operator.le,
    '+': operator.add, '-': operator.sub,
    '*': multiply, '/': operator.truediv,
    # element wise
    '.+': np.add, '.-': np.subtract,
    '.*': np.multiply, './': np.divide
}

unary = {
    '-': operator.neg,
    'TRANSPOSE': np.transpose
}


def zeros(*args):
    if len(args) == 1:
        return np.zeros(args*2)
    else:
        return np.zeros(args)


def ones(*args):
    if len(args) == 1:
        return np.ones(args*2)
    else:
        return np.ones(args)


def return_(value):
    raise ReturnValueException(value)


funcs = {
    'eye': np.eye,
    'zeros': zeros,
    'ones': ones,
    'print': print,
    'return': return_,
}


class Node(metaclass=ABCMeta):
    def __init__(self, line, parent=None):
        self.value = None
        self.parent = parent if parent is not None else self
        self.line_no = line
        # if self.parent != self:
        #     self.public_names.update(self.parent.public_names)
        #     self.parent.add_child(self)

    def attach_parent(self, parent):
        self.parent = parent
        # self.names.update(parent.names)
        # self.public_names.update(parent.public_names)

    def __str__(self):
        return self.format(0)

    def print_tree(self):
        print(self)

    def accept(self, visitor):
        return visitor.visit(self)


class List(Node):
    def __init__(self, line, parent=None):
        super().__init__(line, parent)
        self.children = []

    def add_child(self, child):
        self.children.append(child)


class Lval(Node):
    def __init__(self, line, obj, index=None):
        super().__init__(line)
        self.obj = obj
        self.index = index


class Binop(Node):
    def __init__(self, line, op, left: Node, right: Node):
        super().__init__(line)
        self.op = op
        self.func = operators[op]
        self.left = left
        self.right = right
        self.left.attach_parent(self)
        self.right.attach_parent(self)


class Unop(Node):
    def __init__(self, line, op, var: Node):
        super().__init__(line)
        self.op = op
        self.func = unary[op]
        self.var = var
        self.var.attach_parent(self)


class Assignment(Node):
    def __init__(self, line, var: Lval, value: Node, mode):
        super().__init__(line)
        self.left = var
        if mode == '=':
            self.right = value
        else:
            self.right = Binop(line, mode[:-1], var, value)


class IfElse(Node):
    def __init__(self, line, cond, if_block, else_block=None):
        super().__init__(line)
        self.condition = cond
        self.if_block = if_block
        self.else_block = else_block


class Literal(Node):
    def __init__(self, line, value):
        super().__init__(line)
        self.context = None
        self.value = value
        self.val_type = type(value)
        if self.val_type == np.array:
            self.val_type = np.ndarray
        if self.val_type == np.ndarray:
            self.context = (value.dtype, value.shape)


class WhileLoop(Node):
    def __init__(self, line, condition, block):
        super().__init__(line)
        self.condition = condition
        self.block = block


class ForLoop(Node):
    def __init__(self, line, varname, range_arg, block):
        super().__init__(line)
        self.varname = varname
        self.range_arg = range_arg
        self.block = block


class Range(Node):
    def __init__(self, line, start, end):
        super().__init__(line)
        self.start = start
        self.end = end


class Function(Node):
    def __init__(self, line, name=None):
        """argumenty dodawane w innych punktach parsingu"""
        super().__init__(line)
        self.name = name
        self.args = List(self.line_no)


class BreakCont(Node):
    def __init__(self, line, is_break):
        super().__init__(line)
        self.is_break = is_break

    @property
    def name(self):
        return 'break' if self.is_break else 'continue'
