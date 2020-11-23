from abc import abstractmethod, ABCMeta
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

    @abstractmethod
    def format(self, depth):
        pass

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

    def format(self, depth):
        ret = []
        for child in self.children:
            ret.append(child.format(depth))
        return ''.join(ret)


class Lval(Node):
    def __init__(self, obj, index=None):
        super().__init__()
        self.obj = obj
        self.index = index

    def eval(self):
        raise NotImplementedError('Not ready yet!')

    def format(self, depth):
        ret = '| ' * depth + 'REF\n' + '| ' * (depth + 1) + self.obj + '\n'
        if self.index is not None:
            for a in self.index:
                ret += '| ' * (depth + 1) + str(a) + '\n'
        return ret


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

    def format(self, depth):
        ret = ('| ' * depth + self.op + '\n'
               + self.left.format(depth + 1)
               + self.right.format(depth + 1))
        return ret


class Unop(Node):
    def __init__(self, op, var: Node):
        super().__init__(None)
        self.op = op
        self.func = unary[op]
        self.var = var
        self.var.attach_parent(self)

    def format(self, depth):
        ret = ('| ' * depth + self.op + '\n'
               + self.var.format(depth + 1))
        return ret


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

    def format(self, depth):
        ret = ('| ' * depth + '=' + '\n'
               + self.left.format(depth + 1)
               + self.right.format(depth + 1))
        return ret


class IfElse(Node):
    def __init__(self, cond, if_block, else_block=None):
        super().__init__()
        self.condition = cond
        self.if_block = if_block
        self.else_block = else_block

    def eval(self):
        raise NotImplementedError('Not ready yet!')

    def format(self, depth):
        return ('| ' * depth + 'IF\n'
                + self.condition.format(depth + 1)
                + self.if_block.format(depth + 1)
                + (self.else_block.format(depth + 1)
                   if self.else_block is not None else ''))


class Literal(Node):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def eval(self):
        raise NotImplementedError('Not ready yet!')

    def format(self, depth):
        # inspect.isclass(self.value) returns False for self.value that is Lval :c
        if isinstance(self.value, Lval):
            return self.value.format(depth)
        else:
            return '| ' * depth + str(self.value) + '\n'


class WhileLoop(Node):
    def __init__(self, condition, block):
        super().__init__()
        self.condition = condition
        self.block = block

    def eval(self):
        raise NotImplementedError('Not ready yet!')

    def format(self, depth):
        ret = ('| ' * depth + 'WHILE' + '\n'
               + self.condition.format(depth + 1)
               + self.block.format(depth + 1)
               )
        return ret


class ForLoop(Node):
    def __init__(self, varname, range_arg, block):
        super().__init__()
        self.varname = varname
        self.range_arg = range_arg
        self.block = block

    def eval(self):
        raise NotImplementedError('Not ready yet!')

    def format(self, depth):
        ret = ('| ' * depth + 'FOR' + '\n'
               + self.varname.format(depth + 1)
               + self.range_arg.format(depth + 1)
               + self.block.format(depth + 1)
               )
        return ret


class Range(Node):
    def __init__(self, start, end):
        super().__init__()
        self.start = start
        self.end = end

    def eval(self):
        raise NotImplementedError('Not ready yet!')

    def format(self, depth):
        ret = ('| ' * depth + 'RANGE' + '\n'
               + '| ' * (depth + 1) + str(self.start)
               + '| ' * (depth + 1) + str(self.end)
               )
        return ret


class Function(Node):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.args = List()

    def eval(self):
        raise NotImplementedError('Not ready yet!')

    def format(self, depth):
        ret = ('| ' * depth + self.name + '\n'
               + self.args.format(depth + 1)
               )
        return ret


class BreakCont(Node):
    def __init__(self, is_break):
        super().__init__()
        self.is_break = is_break

    def eval(self):
        raise NotImplementedError('Not ready yet!')

    def format(self, depth):
        return '| ' * depth + ('BREAK\n' if self.is_break else 'CONTINUE\n')
