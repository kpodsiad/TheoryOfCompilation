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
    def __init__(self, line, parent=None):
        self.value = None
        self.public_names = {}
        self.names = {}
        self.parent = parent if parent is not None else self
        self.line_no = line
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
    def __init__(self, line, parent=None):
        super().__init__(line, parent)
        self.children = []

    def eval(self):
        for child in self.children:
            child.public_names.update(self.public_names)
            child.eval()
            self.public_names.update(child.public_names)

    def add_child(self, child):
        self.children.append(child)


class Lval(Node):
    def __init__(self, line, obj, index=None):
        super().__init__(line)
        self.obj = obj
        self.index = index

    def eval(self):
        raise NotImplementedError('Not ready yet!')


class Binop(Node):
    def __init__(self, line, op, left: Node, right: Node):
        super().__init__(line)
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
            self.right = Binop(mode[:-1], var, value)

    def eval(self):
        raise NotImplementedError('Not ready yet!')


class IfElse(Node):
    def __init__(self, line, cond, if_block, else_block=None):
        super().__init__(line)
        self.condition = cond
        self.if_block = if_block
        self.else_block = else_block

    def eval(self):
        raise NotImplementedError('Not ready yet!')


class Literal(Node):
    def __init__(self, line, value):
        super().__init__(line)
        self.context = None
        self.value = value
        self.val_type = type(value)
        if self.val_type == np.array:
            self.context = (value.dtype, value.shape)

    def eval(self):
        raise NotImplementedError('Not ready yet!')


class WhileLoop(Node):
    def __init__(self, line, condition, block):
        super().__init__(line)
        self.condition = condition
        self.block = block

    def eval(self):
        raise NotImplementedError('Not ready yet!')


class ForLoop(Node):
    def __init__(self, line, varname, range_arg, block):
        super().__init__(line)
        self.varname = varname
        self.range_arg = range_arg
        self.block = block

    def eval(self):
        raise NotImplementedError('Not ready yet!')


class Range(Node):
    def __init__(self, line, start, end):
        super().__init__(line)
        self.start = start
        self.end = end

    def eval(self):
        raise NotImplementedError('Not ready yet!')


class Function(Node):
    def __init__(self, line, name=None):
        super().__init__(line)
        self.name = name
        self.args = List(self.line_no)

    def eval(self):
        raise NotImplementedError('Not ready yet!')


class BreakCont(Node):
    def __init__(self, line, is_break):
        super().__init__(line)
        self.is_break = is_break
        
    @property
    def name(self):
        return 'break' if self.is_break else 'continue'

    def eval(self):
        raise NotImplementedError('Not ready yet!')
