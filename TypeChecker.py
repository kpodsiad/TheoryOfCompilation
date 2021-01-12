import abstractsyntaxtree as AST
from itertools import product
from numpy import array, int64, float64, unicode_, ndarray
from sys import stderr

binop_type = {op: {first: {}} for op, first in product(
    AST.operators.keys(), [int, float, str, ndarray])}

for op in AST.operators.keys():
    binop_type[op] = {}
    for first in [int, float, str, ndarray]:
        binop_type[op][first] = {}
        


binop_type['+'][str][str] = str

binop_type['+'][int][int] = int
binop_type['+'][int][float] = float
binop_type['+'][float][int] = float
binop_type['+'][float][float] = float
binop_type['-'][int][int] = int
binop_type['-'][int][float] = float
binop_type['-'][float][int] = float
binop_type['-'][float][float] = float
binop_type['/'][int][int] = int
binop_type['/'][int][float] = float
binop_type['/'][float][int] = float
binop_type['/'][float][float] = float
binop_type['*'][int][int] = int
binop_type['*'][int][float] = float
binop_type['*'][float][int] = float
binop_type['*'][float][float] = float
binop_type['+'][ndarray][ndarray] = ndarray
binop_type['-'][ndarray][ndarray] = ndarray
binop_type['*'][ndarray][ndarray] = ndarray

binop_type['.+'][int][int] = int
binop_type['.+'][int][float] = float
binop_type['.+'][float][int] = float
binop_type['.+'][float][float] = float
binop_type['.-'][int][int] = int
binop_type['.-'][int][float] = float
binop_type['.-'][float][int] = float
binop_type['.-'][float][float] = float
binop_type['./'][int][int] = int
binop_type['./'][int][float] = float
binop_type['./'][float][int] = float
binop_type['./'][float][float] = float
binop_type['.*'][int][int] = int
binop_type['.*'][int][float] = float
binop_type['.*'][float][int] = float
binop_type['.*'][float][float] = float

binop_type['.+'][ndarray][int] = ndarray
binop_type['.+'][ndarray][float] = ndarray
binop_type['.+'][ndarray][ndarray] = ndarray
binop_type['.+'][int][ndarray] = ndarray
binop_type['.+'][float][ndarray] = ndarray
binop_type['.-'][ndarray][int] = ndarray
binop_type['.-'][ndarray][float] = ndarray
binop_type['.-'][ndarray][ndarray] = ndarray
binop_type['.-'][int][ndarray] = ndarray
binop_type['.-'][float][ndarray] = ndarray
binop_type['.*'][ndarray][int] = ndarray
binop_type['.*'][ndarray][float] = ndarray
binop_type['.*'][ndarray][ndarray] = ndarray
binop_type['.*'][int][ndarray] = ndarray
binop_type['.*'][float][ndarray] = ndarray
binop_type['./'][ndarray][int] = ndarray
binop_type['./'][ndarray][float] = ndarray
binop_type['./'][ndarray][ndarray] = ndarray
binop_type['./'][int][ndarray] = ndarray
binop_type['./'][float][ndarray] = ndarray

binop_type['<'][int][int] = int
binop_type['<'][int][float] = int
binop_type['<'][float][int] = int
binop_type['<'][float][float] = int
binop_type['<='][int][int] = int
binop_type['<='][int][float] = int
binop_type['<='][float][int] = int
binop_type['<='][float][float] = int
binop_type['>'][int][int] = int
binop_type['>'][int][float] = int
binop_type['>'][float][int] = int
binop_type['>'][float][float] = int
binop_type['>='][int][int] = int
binop_type['>='][int][float] = int
binop_type['>='][float][int] = int
binop_type['>='][float][float] = int
binop_type['=='][int][int] = int
binop_type['=='][int][float] = int
binop_type['=='][float][int] = int
binop_type['=='][float][float] = int
binop_type['!='][int][int] = int
binop_type['!='][int][float] = int
binop_type['!='][float][int] = int
binop_type['!='][float][float] = int


def type_to_str(type_):
    if type_ == ndarray:
        return 'array'
    elif type_ == int:
        return 'int'
    elif type_ == float:
        return 'float'
    elif type_ == str:
        return 'str'
    else:
        return str(type_)

def dtype_to_type(type_):
    if type_ in (int, float, str, ndarray):
        return type_
    if type_.kind in 'SU': # S - (byte-)string, U - Unicode
        return str
    elif type_.kind in 'bui': # b - bool, u - unsigned int, i - signed int
        return int
    elif type_.kind == 'f': # f - floating-point
        return float
    else:
        return None


class NodeVisitor(object):

    def __init__(self):
        self.namespace = [{}] # rekordy nazwa: (typ, [dtype, wymiar jeśli macierz lub lista])
        self.nested_loops = 0
        self.error = False

    def visit(self, node):
        if node is None:
            return (None,)
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    # Called if no explicit visitor function exists for a node.
    def generic_visit(self, node):
        if isinstance(node, list):
            for elem in node:
                self.visit(elem)
        else:
            for child in node.children:
                if isinstance(child, list):
                    for item in child:
                        if isinstance(item, AST.Node):
                            self.visit(item)
                elif isinstance(child, AST.Node):
                    self.visit(child)

    def visit_List(self, node: AST.List):
        self.namespace.append({})
        for child in node.children:
            self.visit(child)
        self.namespace.pop()

    def visit_Lval(self, node: AST.Lval):
        for layer in self.namespace:
            if node.obj in layer:
                ref_info = layer[node.obj]
                if node.index is not None and ref_info[0] != ndarray:
                    print(node.line_no, 'Cannot subscript a scalar', file=stderr)
                    self.error = True
                elif node.index is not None:
                    if len(node.index) > len(ref_info[2]):
                        print(node.line_no, 'Double-subscript on array', file=stderr)
                        self.error = True
                    elif (node.index[0] >= ref_info[2][0]
                          or (len(node.index) == 2 and node.index[1] >= ref_info[2][1])):
                        print(node.line_no, 'Index out of range', file=stderr)
                        self.error = True
                    elif len(node.index) == 1 and len(ref_info[2]) == 2:
                        return ref_info[0], ref_info[1], ref_info[2][:2]
                    else:
                        return (dtype_to_type(ref_info[1]),)
                else:
                    return ref_info
        print(node.line_no, f'Reference error: {node.obj}', file=stderr)
        self.error = True
        return (None,)
    
    
    def visit_Literal(self, node: AST.Literal):
        if node.context:
            return (node.val_type, *node.context)
        return (node.val_type, )


    def visit_Binop(self, node: AST.Binop):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)
        ret_type = None
        ret_context = []
        try:
            ret_type = binop_type[node.op][left_type[0]][right_type[0]]
        except KeyError:
            print(node.line_no, 'Cannot apply binary operation: incompatible operands types: {} and {}'
                  .format(type_to_str(left_type[0]), type_to_str(right_type[0])), file=stderr)
            self.error = True
        
        # [matrix,vector] x [matrix,vector]
        if left_type[0] == right_type[0] == ndarray: 
            try:
                ret_context.append(binop_type[node.op[-1:]][dtype_to_type(left_type[1])][dtype_to_type(right_type[1])])
            except KeyError:
                print(node.line_no, 'Unsupported element types for operator {}: {} and {}'
                      .format(node.op, type_to_str(dtype_to_type(left_type[1])), type_to_str(dtype_to_type(right_type[1]))))
                self.error = True
            left_shape, right_shape = left_type[2], right_type[2]
            # matrix-matrix
            if len(left_shape) == len(right_shape) == 2: 
                (m,n1), (n2,k) = left_shape, right_shape
                if n1 != n2 and node.op == '*':
                    print(node.line_no, 'Operands could not be broadcast together with shapes {} {}'
                          .format(left_shape, right_shape), file=stderr)
                    self.error = True
                elif left_shape != right_shape:
                    print(node.line_no, 'Operands could not be broadcast together with shapes {} {}'
                          .format(left_shape, right_shape), file=stderr)
                    self.error = True
                elif node.op == '/':
                    print(node.line_no, 'Cannot divide by matrix', file=stderr)
                    self.error = True
                elif node.op == '*':
                    ret_context.append((m, k))
                else:
                    ret_context.append(left_shape)
            # vector-matrix
            elif len(left_shape) == 1: 
                (n1,), (n2, k) = left_shape, right_shape
                if n1 != n2 and node.op == '*':
                    print(node.line_no, 'Operands could not be broadcast together with shapes {} {}'
                          .format(left_shape, right_shape), file=stderr)
                    self.error = True
                elif (1,)+left_shape != right_shape:
                    print(node.line_no, 'Operands could not be broadcast together with shapes {} {}'
                          .format(left_shape, right_shape), file=stderr)
                    self.error = True
                elif node.op == '/':
                    print(node.line_no, 'Cannot divide by matrix', file=stderr)
                    self.error = True
                elif node.op == '*':
                    ret_context.append((1, k))
                else:
                    ret_context.append(right_shape)
            # matrix-vector
            elif len(right_shape) == 1:
                (m, n1), (n2,) = left_shape, right_shape
                if n1 != 1 and node.op == '*':
                    print(node.line_no, 'Operands could not be broadcast together with shapes {} {}'
                          .format(left_shape, right_shape), file=stderr)
                    self.error = True
                elif node.op == '/':
                    print(node.line_no, 'Cannot divide by vector', file=stderr)
                    self.error = True
                elif node.op == '*':
                    ret_context.append((m, n2))
                else:
                    ret_context.append(left_shape)
            # vector-vector
            else:
                (n1,), (n2,) = left_shape, right_shape
                if n1 != n2:
                    print(node.line_no, 'Operands could not be broadcast together with shapes {} {}'
                          .format(left_shape, right_shape), file=stderr)
                    self.error = True
                elif node.op == '/':
                    print(node.line_no, 'Cannot divide by vector', file=stderr)
                    self.error = True
                elif node.op == '*':
                    ret_context.append((1,1))
                else:
                    ret_context.append(left_shape)
        # number-number
        elif left_type[0] in {int, float} and right_type[0] in {int,float}:  
            if node.op in {'.+', '.-', '.*', './'}:
                print(node.line_no, 'Cannot apply dot operator to numbers', file=stderr)
                self.error = True
        # str-str
        elif left_type[0] == right_type[0] == str:
            if node.op != '+':
                print(node.line_no, 'Cannot apply operator to string. Strings supports concatenation', file=stderr)
                self.error = True
        
        return (ret_type, *ret_context)

    def visit_Unop(self, node: AST.Unop):
        val_type = self.visit(node.var)
        if node.op == "'":
            if val_type[0]==ndarray:
                return val_type
            else:
                print(node.line_no, 'Type mismatch for operator \': {}'
                      .format(type_to_str(val_type[0])), file=stderr)
                self.error = True
        elif node.op == '-':
            if val_type[0] != str:
                return val_type
            else:
                print(node.line_no, 'Type mismatch for operator - (unary): {}'
                      .format(type_to_str(val_type[0])), file=stderr)
                self.error = True
        return (None,)

    def visit_Assignment(self, node: AST.Assignment):
        ref_info = self.visit(node.right)
        old_one = None
        for layer in self.namespace:
            if node.left.obj in layer:
                old_one = layer[node.left.obj]
                layer[node.left.obj] = ref_info
        self.namespace[-1][node.left.obj] = ref_info
        return ref_info
            
            
    def visit_IfElse(self, node: AST.IfElse):
        self.visit(node.condition)
        self.visit(node.if_block)
        if node.else_block is not None:
            self.visit(node.else_block)

    def visit_WhileLoop(self, node: AST.WhileLoop):
        self.visit(node.condition)
        self.nested_loops += 1
        self.visit(node.block)
        self.nested_loops -= 1

    def visit_ForLoop(self, node: AST.ForLoop):
        self.visit(node.range_arg)
        self.nested_loops += 1
        self.namespace.append({node.varname.obj: (int,)})
        self.visit(node.block)
        self.namespace.pop()
        self.nested_loops -= 1

    def visit_Range(self, node: AST.Range):
        left_type = self.visit(node.start)
        right_type = self.visit(node.end)
        if left_type[0] != int or right_type[0] != int:
            print(node.line_no, 'Range values must be integers', file=stderr)
            self.error = True

    def visit_Function(self, node: AST.Function):
        if node.name and node.name != 'print':
            for arg in node.args.children:
                if self.visit(arg)[0] != int:
                    print(node.line_no, 'Arguments for {} must be integral'.format(node.name))
                    self.error = True
            args = tuple(child.value for child in node.args.children)
            if len(args) == 1:
                return (ndarray, int, args*2)
            else:
                return (ndarray, int, args)
        else: 
            return (None,)
    
    def visit_BreakCont(self, node: AST.BreakCont):
        if self.nested_loops == 0:
            print(node.line_no, 'Dangling {} outside of loop'.format(node.name), file=stderr)
            self.error = True


class TypeChecker(NodeVisitor):

    def visit_BinExpr(self, node):
        # alternative usage,
        # requires definition of accept method in class Node
        type1 = self.visit(node.left)     # type1 = node.left.accept(self)
        type2 = self.visit(node.right)    # type2 = node.right.accept(self)
        op = node.op

    def visit_Variable(self, node):
        pass
