from abc import abstractmethod, ABCMeta
import numpy as np
import operator

operators = {
    '==': operator.eq, '!=': operator.ne,
    '>': operator.gt, '<': operator.lt,
    '>=': operator.ge, '<=': operator.le,
    '+': operator.add, '-': operator.sub,
    '.+': operator.add, '.-': operator.sub,
}
unary = {
    '-': operator.neg,
    "'": np.transpose
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

    def attatch_parent(self, parent):
        self.parent = parent
        # self.names.update(parent.names)
        # self.public_names.update(parent.public_names)
    
    @abstractmethod
    def format(self, depth):
        pass
    
    def __str__(self):
        self.format(0)


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


class Lval(Node):
    def __init__(self, object, index=None):
        super().__init__()
        self.object = object
        self.index = index
        
    def eval(self):
        raise NotImplementedError('Not ready yet!')
    
    def format(self, depth):
        ret = '| ' * depth + 'REF\n' + '| ' * (depth+1) + self.object
        if self.index is not None:
            for a in self.index:
                ret += '| ' * (depth+1) + a


class Binop(Node):
    def __init__(self, op, left: Node, right: Node):
        super().__init__(None)
        self.op = op
        self.func = operators[op]
        self.left = left
        self.right = right
        self.left.attatch_parent(self)
        self.right.attatch_parent(self)

    def eval(self):
        self.left.eval()
        self.right.eval()
        self.value = self.func(self.left.value, self.right.value)
        self.public_names = {**left.public_names, **right.public_names}
        self.names = {**left.names, **right.names}
        
    def format(self, depth):
        ret = ('| ' * depth + self.op + '\n' 
               + self.left.format(depth+1) 
               + self.right.format(depth+1))
        

class Unop(Node):
    def __init__(self, op, var: Node):
        super().__init__(None)
        self.func = operators[op]
        self.var = var
        self.var.attatch_parent(self)
    
    def format(self, depth):
        ret = ('| ' * depth + self.op + '\n' 
               + self.var.format(depth+1))
        

class Assignment(Node):
    def __init__(self, var: Lval, value: Node, mode):
        super().__init__()
        self.left = var
        if mode == '=':
            self.right = value
        else:
            self.right = Binop(mode[1:], var, value)

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


class ForLoop(Node):
    def __init__(self, varname, range, block):
        super().__init__()
        self.varname = varname
        self.range = range
        self.block = block
        

class Range(Node):
    def __init__(self, start, end):
        super().__init__()
        self.start = start
        self.end = end
