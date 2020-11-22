#!/usr/bin/python

import scanner
import ply.yacc as yacc
import numpy as np
import abstractsyntaxtree as ast

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
)


def p_error(p):
    if p:
        print('Syntax error at line {0}, column {1}: LexToken({2}, \'{3}\')'.format(
            p.lineno, scanner.find_tok_column(p), p.type, p.value))
    else:
        print('Unexpected end of input')


def p_program(p):
    """program : instructions_opt"""


def p_instructions_opt_1(p):
    """instructions_opt : instructions """


def p_instructions_opt_2(p):
    """instructions_opt : """


def p_instructions_1(p):
    """instructions : instructions instruction """


def p_instructions_2(p):
    """instructions : instruction """


def p_instruction(p):
    """instruction : code_block
                   | generic_expression ';'
                   | flow_control
                   | BREAK ';'
                   | CONTINUE ';' """


def p_code_block(p):
    """code_block : '{' instructions_opt '}'"""


def p_generic_expression(p):
    """generic_expression : assignment
                          | print_expr
                          | RETURN expression
    """


def p_print_expr(p):
    """print_expr : PRINT values
       values : value ',' values
              | value
    """


def p_lvalue(p):
    """lvalue : ID
              | ID '[' INT ']' 
              | ID '[' INT ',' INT ']'
    """


def p_assignment(p):
    """assignment : lvalue '=' assignment
                  | lvalue ADDASSIGN assignment
                  | lvalue SUBASSIGN assignment
                  | lvalue MULASSIGN assignment
                  | lvalue DIVASSIGN assignment
                  | expression
    """
    if len(p) == 4:
        p[0] = ast.ASTAssignment()


def p_expression_binop(p):
    """expression : expression '+' expression
                  | expression '-' expression
                  | expression '*' expression
                  | expression '/' expression
                  | expression DOTADD expression
                  | expression DOTSUB expression
                  | expression DOTMUL expression
                  | expression DOTDIV expression"""


def p_expression_relop(p):
    """expression : expression GE expression
                  | expression GT expression
                  | expression LE expression
                  | expression LT expression
                  | expression EQ expression
                  | expression NE expression"""


def p_expression_uminus(p):
    """expression : - expression %prec UMINUS"""
    p[0] = '-' + p[1]
      
                  
def p_expression_transposition(p):
    """expression : expression TRANSPOSITION"""
    p[0] = p[2] + "'"
       
                  
def p_expression_downgrade(p):
    """expression : value
                  | func_call
                  | '(' assignment ')'"""


def p_primitive(p):
    """number    : INT
                 | FLOAT
       primitive : number
                 | STR"""
    p[0] = p[1]


def p_matrix(p):
    """matrix      : '[' matrix_rows ']'
       matrix_rows : row ',' matrix_rows
                   | row"""
    if len(p) == 2: # matrix_rows : row
        p[0] = [p[1]]
    elif p[2] == ',': # matrix_rows : row ',' matrix_rows
        p[0] = [p[1]] + p[3]
    else: # matrix : '[' matrix_rows ']'
        p[0] = np.array(p[2])
        
        
def p_row(p):
    """row        : '[' primitives ']'
       primitives : primitive ',' primitives
                  | primitive"""
    if len(p) == 2: # primitives : primitive
        p[0] = [p[1]]
    elif p[2] == ',': # primitives : primitive ',' primitives
        p[0] = [p[1]] + p[3]
    else: # row : '[' primitives ']'
        p[0] = np.array(p[2])
                   

def p_value(p):
    """value : matrix
             | primitive
             | lvalue
             | row"""
    p[0] = ast.ASTLiteral(p[1])

             
def p_func_call(p):
    """func_call : EYE '(' INT ')'
                 | ONES '(' INT ')'
                 | ONES '(' INT ',' INT ')'
                 | ZEROS '(' INT ')'
                 | ZEROS '(' INT ',' INT ')'
    """
    if p[1] == 'eye':
        p[0] = np.eye(p[3])
    elif p[1] == 'ones':
        if len(p) == 5: # 1 arg
            p[0] = np.ones((p[3], p[3]))
        else: # 2 arg
            p[0] = np.ones((p[3], p[5]))
    else: # zeros
        if len(p) == 5:
            p[0] = np.zeros((p[3], p[3]))
        else:
            p[0] = np.zeros((p[3], p[5]))
        


def p_flow_control(p):
    """flow_control : IF '(' assignment ')' instruction %prec IFX
                    | IF '(' assignment ')' instruction ELSE instruction
                    | WHILE '(' assignment ')' instruction
                    | IF '(' error ')' instruction %prec IFX
                    | IF '(' error ')' instruction ELSE instruction
                    | WHILE '(' error ')' instruction
                    | FOR ID '=' range instruction
       range        : id_or_int ':' id_or_int
       id_or_int    : ID
                    | INT
    """
    if p[1] == 'if':
        p[0] = ast.ASTFlowControl
    


parser = yacc.yacc()
# https://stackoverflow.com/questions/51575487/python-lex-yacc-reports-infinite-recursion-detected-for-symbol
# https://stackoverflow.com/questions/61751397/resolving-shift-reduce-conflicts-in-ply-yacc
