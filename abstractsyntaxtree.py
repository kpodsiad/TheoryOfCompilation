from abc import ABCMeta
import numpy as np
import operator

operators = {
    '==': operator.eq, '!=': operator.ne,
    '>': operator.gt, '<': operator.lt,
    '>=': operator.ge, '<=': operator.le,
    '+': operator.add, '-': operator.sub,
    '.+': operator.add, '.-': operator.sub,
    '*': operator.mul, '/': operator.truediv,
    '.*': operator.mul, './': operator.truediv
}
unary = {
    '-': operator.neg,
    'TRANSPOSE': np.transpose
}


class Node(metaclass=ABCMeta):
    def __init__(self, parent=None):
        self.value = None
        self.public_names = {}
        self.names = {}
        self.parent = parent if parent is not None else self
        # if self.parent != self:
        #     self.public_names.update(self.parent.public_names)
        #     self.parent.add_child(self)

    '''@abstractmethod
    def eval(self):
        self.public_names.update(self.parent.public_names)'''

    def attach_parent(self, parent):
        self.parent = parent
        # self.names.update(parent.names)
        # self.public_names.update(parent.public_names)

    def __str__(self):
        return self.format(0)

    def print_tree(self):
        print(self)


class List(Node):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.children = []

    def eval(self):
        for child in self.children:
            child.public_names.update(self.public_names)
            child.eval()
            self.public_names.update(child.public_names)

    def add_child(self, child):
        self.children.append(child)


class Lval(Node):
    def __init__(self, obj, index=None):
        super().__init__()
        self.obj = obj
        self.index = index

    def eval(self):
        raise NotImplementedError('Not ready yet!')


class Binop(Node):
    def __init__(self, op, left: Node, right: Node):
        super().__init__(None)
        self.op = op
        self.func = operators[op]
        self.left = left
        self.right = right
        self.left.attach_parent(self)
        self.right.attach_parent(self)

    def eval(self):
        self.left.eval()
        self.right.eval()
        self.value = self.func(self.left.value, self.right.value)
        self.public_names = {**self.left.public_names, **self.right.public_names}
        self.names = {**self.left.names, **self.right.names}


class Unop(Node):
    def __init__(self, op, var: Node):
        super().__init__(None)
        self.op = op
        self.func = unary[op]
        self.var = var
        self.var.attach_parent(self)


class Assignment(Node):
    def __init__(self, var: Lval, value: Node, mode):
        super().__init__()
        self.left = var
        if mode == '=':
            self.right = value
        else:
            self.right = Binop(mode[:-1], var, value)

    def eval(self):
        raise NotImplementedError('Not ready yet!')


class IfElse(Node):
    def __init__(self, cond, if_block, else_block=None):
        super().__init__()
        self.condition = cond
        self.if_block = if_block
        self.else_block = else_block

    def eval(self):
        raise NotImplementedError('Not ready yet!')


class Literal(Node):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def eval(self):
        raise NotImplementedError('Not ready yet!')


class WhileLoop(Node):
    def __init__(self, condition, block):
        super().__init__()
        self.condition = condition
        self.block = block

    def eval(self):
        raise NotImplementedError('Not ready yet!')


class ForLoop(Node):
    def __init__(self, varname, range_arg, block):
        super().__init__()
        self.varname = varname
        self.range_arg = range_arg
        self.block = block

    def eval(self):
        raise NotImplementedError('Not ready yet!')


class Range(Node):
    def __init__(self, start, end):
        super().__init__()
        self.start = start
        self.end = end

    def eval(self):
        raise NotImplementedError('Not ready yet!')


class Function(Node):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.args = List()

    def eval(self):
        raise NotImplementedError('Not ready yet!')


class BreakCont(Node):
    def __init__(self, is_break):
        super().__init__()
        self.is_break = is_break

    def eval(self):
        raise NotImplementedError('Not ready yet!')

    def format(self, depth):
        return '| ' * depth + ('BREAK\n' if self.is_break else 'CONTINUE\n')
