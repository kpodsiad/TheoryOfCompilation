#!/usr/bin/python

import scanner
import ply.yacc as yacc
import numpy as np
import abstractsyntaxtree as ast

from sys import stderr
from warnings import filterwarnings
filterwarnings('error', category=np.VisibleDeprecationWarning)


tokens = scanner.tokens

precedence = (
    ('nonassoc', 'IFX'),
    ('nonassoc', 'ELSE'),
    ('right', '=', 'ADDASSIGN', 'SUBASSIGN', 'MULASSIGN', 'DIVASSIGN'),
    ('left', 'EQ', 'NE'),
    ('left', 'GE', 'LE', 'LT', 'GT'),
    ('left', '+', '-', 'DOTADD', 'DOTSUB'),
    ('left', '*', '/', 'DOTMUL', 'DOTDIV'),
    ('right', 'UMINUS'),
    ('right', 'TRANSPOSITION'),
)


def p_error(p):
    if p:
        print('Syntax error at line {0}, column {1}: LexToken({2}, \'{3}\')'.format(
            p.lexer.lineno, scanner.find_tok_column(p), p.type, p.value))
    else:
        print('Unexpected end of input')


def p_program(p):
    """program : instructions_opt
    """
    p[0] = p[1]


def p_instructions_opt_1(p):
    """instructions_opt : instructions """
    p[0] = p[1]


def p_instructions_opt_2(p):
    """instructions_opt : """
    p[0] = ast.List(p.lexer.lineno)


def p_instructions_1(p):
    """instructions : instructions instruction """
    p[1].add_child(p[2])
    p[0] = p[1]


def p_instructions_2(p):
    """instructions : instruction """
    p[0] = ast.List(p.lexer.lineno)
    p[0].add_child(p[1])


def p_instruction(p):
    """instruction : code_block
                   | generic_expression ';'
                   | flow_control
                   | BREAK ';'
                   | CONTINUE ';' """
    if p[1] in {'continue', 'break'}:
        p[0] = ast.BreakCont(p.slice[1].lineno, p[1] == 'break')
    else:
        p[0] = p[1]


def p_code_block(p):
    """code_block : '{' instructions_opt '}'
    """
    p[0] = p[2]


def p_generic_expression(p):
    """generic_expression : assignment
                          | print_expr
                          | RETURN expression
    """
    if p[1] == 'return':
        p[0] = ast.Function(p.lexer.lineno)
        p[0].args.add_child(p[2])
    else:
        p[0] = p[1]
    


def p_print_expr(p):
    """print_expr : PRINT values
    """
    p[0] = ast.Function(p.lexer.lineno, 'print')
    p[0].args = p[2]
    
        

def p_values_list(p):
    """values : values ',' value
              | value
    """
    if len(p) == 2:
        p[0] = ast.List(p.lexer.lineno)
        p[0].add_child(p[1])
    else:
        p[0] = p[1]
        p[1].add_child(p[3])

def p_lvalue(p):
    """lvalue : ID
              | ID '[' INT ']' 
              | ID '[' INT ',' INT ']'
    """
    l = len(p)
    if l == 2:
        p[0] = ast.Lval(p.lexer.lineno, p[1])
    elif l == 5:
        p[0] = ast.Lval(p.lexer.lineno, p[1], (p[3],))
    else:
        p[0] = ast.Lval(p.lexer.lineno, p[1], (p[3], p[5]))


def p_assignment(p):
    """assignment : lvalue '=' assignment
                  | lvalue ADDASSIGN assignment
                  | lvalue SUBASSIGN assignment
                  | lvalue MULASSIGN assignment
                  | lvalue DIVASSIGN assignment
                  | expression
    """
    if len(p) == 4:
        p[0] = ast.Assignment(p.lexer.lineno, p[1], p[3], p[2])
    else:
        p[0] = p[1]


def p_expression_binop(p):
    """expression : expression '+' expression
                  | expression '-' expression
                  | expression '*' expression
                  | expression '/' expression
                  | expression DOTADD expression
                  | expression DOTSUB expression
                  | expression DOTMUL expression
                  | expression DOTDIV expression
                  | expression GE expression
                  | expression GT expression
                  | expression LE expression
                  | expression LT expression
                  | expression EQ expression
                  | expression NE expression
    """
    p[0] = ast.Binop(p.lexer.lineno, p[2], p[1], p[3])


def p_expression_uminus(p):
    """expression : - expression %prec UMINUS
    """
    p[0] = ast.Unop(p.lexer.lineno, '-', p[2])


def p_expression_transposition(p):
    """expression : expression TRANSPOSITION
    """
    p[0] = ast.Unop(p.lexer.lineno, 'TRANSPOSE', p[1])


def p_expression_downgrade(p):
    """expression : value
                  | func_call
                  | '(' expression ')'
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]


def p_value(p):
    """value : matrix
             | primitive
             | lvalue
             | row
    """
    if type(p[1]) == ast.Lval:
        p[0] = p[1]
    else:
        p[0] = ast.Literal(p.lexer.lineno, p[1])


def p_primitive(p):
    """primitive : number
                 | STR
    """
    p[0] = p[1]
    

def p_number(p):
    """number    : INT
                 | FLOAT
    """
    p[0] = p[1]


def p_matrix(p):
    """matrix      : '[' matrix_rows ']'
    """
    try:
        p[0] = np.array(p[2])
    except np.VisibleDeprecationWarning:
        print(p.lexer.lineno, 'Cannot define non-rectangular matrix', file=stderr)
        p[0] = None
        

def p_matrix_rows(p):
    """matrix_rows : row ',' matrix_rows
                   | row
    """
    if len(p) == 2:  # matrix_rows : row
        p[0] = [p[1]]
    elif p[2] == ',':  # matrix_rows : row ',' matrix_rows
        p[0] = [p[1]] + p[3]


def p_row(p):
    """row        : '[' primitives ']'
    """
    p[0] = np.array(p[2])
        

def p_primitives(p):
    """primitives : primitive ',' primitives
                  | primitive
    """
    if len(p) == 2:  # primitives : primitive
        p[0] = [p[1]]
    else:  # primitives : primitive ',' primitives
        p[0] = [p[1]] + p[3]


def p_func_call(p):
    """func_call : EYE '(' INT ')'
                 | ONES '(' INT ')'
                 | ONES '(' INT ',' INT ')'
                 | ZEROS '(' INT ')'
                 | ZEROS '(' INT ',' INT ')'
    """
    p[0] = ast.Function(p.lexer.lineno, p[1])
    p[0].args.add_child(ast.Literal(p.lexer.lineno, p[3]))
    if len(p) == 7:  # 2 arg
        p[0].args.add_child(ast.Literal(p.lexer.lineno, p[5]))


def p_flow_control(p):
    """flow_control : IF '(' expression ')' instruction %prec IFX
                    | IF '(' expression ')' instruction ELSE instruction
                    | WHILE '(' expression ')' instruction
                    | IF '(' error ')' instruction %prec IFX
                    | IF '(' error ')' instruction ELSE instruction
                    | WHILE '(' error ')' instruction
                    | FOR ID '=' range instruction
    """
    if p[1] == 'if':
        p[0] = ast.IfElse(p.lexer.lineno, p[3], p[5], p[7] if len(p) == 8 else None)
    elif p[1] == 'while':
        p[0] = ast.WhileLoop(p.lexer.lineno, p[3], p[5])
    else:
        p[0] = ast.ForLoop(p.lexer.lineno, ast.Lval(p.lexer.lineno, p[2]), p[4], p[5])


def p_range(p):
    """range : id_or_int ':' id_or_int
    """
    p[0] = ast.Range(p.lexer.lineno, p[1], p[3])


def p_id_or_int_id(p):
    """id_or_int : ID
    """
    p[0] = ast.Lval(p.lexer.lineno, p[1])
    
def p_id_or_int_int(p):
    """id_or_int : INT
    """
    p[0] = ast.Literal(p.lexer.lineno, p[1])


parser = yacc.yacc()


# https://stackoverflow.com/questions/51575487/python-lex-yacc-reports-infinite-recursion-detected-for-symbol
# https://stackoverflow.com/questions/61751397/resolving-shift-reduce-conflicts-in-ply-yacc
