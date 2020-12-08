import abstractsyntaxtree as AST


def addToClass(cls):

    def decorator(func):
        setattr(cls,func.__name__,func)
        return func
    return decorator


class TreePrinter:
    @addToClass(AST.Node)
    def print_tree(self):
        print(self.format(0))

    @addToClass(AST.List)
    def format(self: AST.List, depth):
        ret = []
        for child in self.children:
            ret.append(child.format(depth))
        return ''.join(ret)

    @addToClass(AST.Lval)
    def format(self: AST.Lval, depth):
        ret = '| ' * depth + 'REF\n' + '| ' * (depth + 1) + self.obj + '\n'
        if self.index is not None:
            for a in self.index:
                ret += '| ' * (depth + 1) + str(a) + '\n'
        return ret

    @addToClass(AST.Binop)
    def format(self: AST.Binop, depth):
        ret = ('| ' * depth + self.op + '\n'
               + self.left.format(depth + 1)
               + self.right.format(depth + 1))
        return ret

    @addToClass(AST.Unop)
    def format(self: AST.Unop, depth):
        ret = ('| ' * depth + self.op + '\n'
               + self.var.format(depth + 1))
        return ret

    @addToClass(AST.Assignment)
    def format(self: AST.Assignment, depth):
        ret = ('| ' * depth + '=' + '\n'
               + self.left.format(depth + 1)
               + self.right.format(depth + 1))
        return ret

    @addToClass(AST.IfElse)
    def format(self: AST.IfElse, depth):
        return ('| ' * depth + 'IF\n'
                + self.condition.format(depth + 1)
                + self.if_block.format(depth + 1)
                + (self.else_block.format(depth + 1)
                   if self.else_block is not None else ''))

    @addToClass(AST.Literal)
    def format(self: AST.Literal, depth):
        # inspect.isclass(self.value) returns False for self.value that is Lval :c
        if isinstance(self.value, AST.Lval):
            return self.value.format(depth)
        else:
            return '| ' * depth + str(self.value) + '\n'

    @addToClass(AST.WhileLoop)
    def format(self: AST.WhileLoop, depth):
        ret = ('| ' * depth + 'WHILE' + '\n'
               + self.condition.format(depth + 1)
               + self.block.format(depth + 1)
               )
        return ret

    @addToClass(AST.ForLoop)
    def format(self: AST.ForLoop, depth):
        ret = ('| ' * depth + 'FOR' + '\n'
               + self.varname.format(depth + 1)
               + self.range_arg.format(depth + 1)
               + self.block.format(depth + 1)
               )
        return ret

    @addToClass(AST.Range)
    def format(self: AST.Range, depth):
        ret = ('| ' * depth + 'RANGE' + '\n'
               + '| ' * (depth + 1) + str(self.start) + '\n'
               + '| ' * (depth + 1) + str(self.end) + '\n'
               )
        return ret

    @addToClass(AST.Function)
    def format(self: AST.Function, depth):
        ret = ('| ' * depth + self.name + '\n'
               + self.args.format(depth + 1)
               )
        return ret

    @addToClass(AST.BreakCont)
    def format(self: AST.BreakCont, depth):
        return '| ' * depth + ('BREAK\n' if self.is_break else 'CONTINUE\n')
