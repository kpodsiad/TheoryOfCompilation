from abc import ABC, abstractmethod
import numpy as np
import operator

operators = {
    '==': operator.eq, '!=': operator.ne,
    '>': operator.gt, '<': operator.lt,
    '>=': operator.ge, '<=': operator.le,
    '+': operator.add, '-': operator.sub,
    '.+': operator.add, '.-': operator.sub,
}


class ASTNode(ABC):
    def __init__(self, parent=None):
        self.value = None
        self.public_names = {}
        self.names = {}
        self.parent = parent if parent is not None else self
        # if self.parent != self:
        #     self.public_names.update(self.parent.public_names)
        #     self.parent.add_child(self)

    @abstractmethod
    def eval(self):
        self.public_names.update(self.parent.public_names)

    def attatch_parent(self, parent):
        self.parent = parent
        # self.names.update(parent.names)
        # self.public_names.update(parent.public_names)


class ASTList(ASTNode):
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


class ASTLval(ASTNode):
    def __init__(self, object, index=None):
        super().__init__()
        self.object = object
        self.index = index
        
    def eval(self):
        raise NotImplementedError('Not ready yet!')


class ASTBinop(ASTNode):
    def __init__(self, op, left: ASTNode, right: ASTNode):
        super().__init__(None)
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


class ASTAssignment(ASTNode):
    def __init__(self, var: ASTLval, value: ASTNode, mode):
        super().__init__()
        self.left = var
        if mode == '=':
            self.right = value
        else:
            self.right = ASTBinop(mode[1:], var, value)

    def eval(self):
        raise NotImplementedError('Not ready yet!')


class ASTFlowControl(ASTNode):
    def __init__(self, cond, if_block, else_block=None):
        super().__init__()
        self.condition = cond
        self.if_block = if_block
        self.else_block = else_block
        
    def eval(self):
        raise NotImplementedError('Not ready yet!')


class ASTLiteral(ASTNode):
    def __init__(self, value):
        super().__init__()
        self.value = value
        
    def eval(self):
        raise NotImplementedError('Not ready yet!')
