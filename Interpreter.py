
import abstractsyntaxtree as AST
# import SymbolTable
from Memory import *
from Exceptions import  *
from visit import *
import sys

sys.setrecursionlimit(10000)

class Interpreter(object):
    
    def __init__(self):
        self.stack = MemoryStack()

    @on('node')
    def visit(self, node):
        pass

    @when(AST.List)
    def visit(self, node):
        ret = []
        for child in node.children:
            ret.append(child.accept(self))

    @when(AST.Lval)
    def visit(self, node):
        if node.index is None:
            return node.obj
        else:
            return node.obj, node.index
        
    @when(AST.Binop)
    def visit(self, node):
        r1 = node.left.accept(self)
        r2 = node.right.accept(self)
        return node.func(r1, r2)

    @when(AST.Unop)
    def visit(self, node):
        r = node.var.accept(self)
        return node.func(r)
        

    @when(AST.Assignment)
    def visit(self, node):
        res = node.left.accept(self)
        value = node.right.accept(self)
        if type(res) == str:
            self.stack.set(res, value)
        else:
            name, index = res
            var = self.stack.get(name)
            var[index] = value
        
    @when(AST.IfElse)
    def visit(self, node):
        decision = node.condition.accept(self)
        self.stack.push(Memory(f'frame{len(self.stack.frames)}_if'))
        r = None
        if bool(decision):
            r = node.if_block.accept(self)
        elif node.else_block is not None:
            r = node.else_block.accept(self)
        self.stack.pop()
        return r
    
    @when(AST.Literal)
    def visit(self, node):
        return node.value
    
    @when(AST.WhileLoop)
    def visit(self, node):
        r = None
        self.stack.push(Memory(f'frame{len(self.stack.frames)}_while'))
        while bool(node.cond.accept(self)):
            try:
                r = node.body.accept(self)
            except BreakException:
                break
            except ContinueException:
                continue
        self.stack.pop()
        return r

    @when(AST.ForLoop)
    def visit(self, node):
        self.stack.push(Memory(f'frame{len(self.stack.frames)}_for'))
        for_var = node.varname.accept(self)
        range_arg = node.range_arg.accept(self)
        self.stack.insert(for_var, None)
        for i in range_arg:
            self.stack.set(for_var, i)
            try:
                node.block.accept(self)
            except BreakException:
                break
            except ContinueException:
                continue
        self.stack.pop()

    
    @when(AST.Range)
    def visit(self, node):
        return range(node.start.accept(self), node.end.accept(self)+1)

    
    @when(AST.Function)
    def visit(self, node):
        args = node.args.accept(self)
        return AST.funcs[node.name](*args)

    
    @when(AST.BreakCont)
    def visit(self, node):
        if node.is_break:
            raise BreakException
        else:
            raise ContinueException
