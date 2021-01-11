
import sys
import ply.yacc as yacc
from Mparser import parser
from scanner import lexer as scanner
from TreePrinter import TreePrinter
from TypeChecker import NodeVisitor
from Interpreter import Interpreter
from Exceptions import ReturnValueException

if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "example.txt"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    text = file.read()
    ast = parser.parse(text, lexer=scanner)
    print(ast)
    visitor = NodeVisitor()
    visitor.visit(ast)

    try:
        ast.accept(Interpreter())
    except ReturnValueException as e:
        print(f'Program returned with value {e.value}')
    # in future
    # ast.accept(OptimizationPass1())
    # ast.accept(OptimizationPass2())
    # ast.accept(CodeGenerator())
    