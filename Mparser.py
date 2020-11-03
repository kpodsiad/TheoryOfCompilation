#!/usr/bin/python

import scanner
import ply.yacc as yacc


tokens = scanner.tokens

precedence = (
    # to fill ...
    ('right', '=', 'ADDASSIGN', 'SUBASSIGN', 'MULASSIGN', 'DIVASSIGN'),
    ('left', 'EQ', 'NE'),
    ('left', 'GE', 'LE', 'LT', 'GT'),
    ('left', '+', '-', 'DOTADD', 'DOTSUB'),
    ('left', '*', '/', 'DOTMUL', 'DOTDIV'),
    ('right', 'UMINUS'),
    # to fill ...
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
                   | generic_expression
                   | flow_control"""


def p_code_block(p):
    """code_block : '{' instructions_opt '}'"""


def p_generic_expression(p):
    """generic_expression : assignment ';'
                          : PRINT STR ';'
                          : RETURN expression ';'
    """


def p_assignment(p):
    """assignment : ID '=' assignment
                  | ID ADDASSIGN assignment
                  | ID SUBASSIGN assignment
                  | ID MULASSIGN assignment
                  | ID DIVASSIGN assignment
    """


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


def p_expression_group(p):
    """expression : '(' expression ')'"""
    p[0] = p[2]


def p_expression_uminus(p):
    """expression : - expression %prec UMINUS"""
    p[0] = '-' + p[2]  # inaczej python pluł się, że operator - jest używany ze złym typem
    
    
def p_expression_comp(p):
    """expression : expression LT expression
                  | expression GT expression
                  | expression EQ expression
                  | expression NE expression
                  | expression LE expression
                  | expression GE expression"""
       
                  
def p_expression_transposition(p):
    """expression : expression TRANSPOSITION"""
    p[0] = p[2] + "'"
       
                  
def p_expression_downgrade(p):
    """expression : primitive
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
       matrix_rows : matrix_row ',' matrix_rows
                   |
       matrix_row  : '[' primitives ']'
       primitives  : primitive ',' primitives
                   | """
    # nie jestem 100% pewien pod kątem tej definicji


def p_value(p):
    """value : matrix
             | primitive"""
             
def p_func_call(p):
    """func_call : EYE '(' INT ')'
                 | ONES '(' INT ')'
                 | ONES '(' INT ',' INT ')'
                 | ZEROS '(' INT ')'
                 | ZEROS '(' INT ',' INT ')'
    """


parser = yacc.yacc()
