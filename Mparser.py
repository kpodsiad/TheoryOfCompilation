#!/usr/bin/python

import scanner
import ply.yacc as yacc


tokens = scanner.tokens

precedence = (
    # to fill ...
    ('left', '+', '-', 'DOTADD', 'DOTSUB'),
    ('left', '*', '/', 'DOTMUL', 'DOTDIV'),
    ('left', 'TRANSPOSITION'),
    ('right', 'UMINUS'),
    ('left', 'GE', 'LE', 'LT', 'GT', 'EQ', 'NE'),
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


# to finish the grammar
# ....


def p_instruction(p):
    """instruction : code_block
                   | generic_expression ';'
                   | flow_control"""


def p_code_block(p):
    """code_block : '{' instructions_opt '}'"""


def p_generic_expression(p):
    """generic_expression : assignment
                          | expression
                          | func_call"""


def p_assignment(p):
    """assignment : ID '=' generic_expression
                  | ID ADDASSIGN generic_expression
                  | ID SUBASSIGN generic_expression
                  | ID MULASSIGN generic_expression
                  | ID DIVASSIGN generic_expression"""


def p_expression_group(p):
    """expression : '(' expression ')'"""
    p[0] = p[2]


def p_expression_binop(p):
    """expression : expression '+' expression
                  | expression '-' expression
                  | expression '*' expression
                  | expression '/' expression"""
    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]
    elif p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        p[0] = p[1] / p[3]


def p_expression_dotbinop(p):
    """expression : expression DOTADD expression
                  | expression DOTSUB expression
                  | expression DOTMUL expression
                  | expression DOTDIV expression"""
    # todo: what to do below?
    if p[2] == '.+':
        p[0] = p[1] + p[3]
    elif p[2] == '.-':
        p[0] = p[1] - p[3]
    elif p[2] == '.*':
        p[0] = p[1] * p[3]
    elif p[2] == './':
        p[0] = p[1] / p[3]


def p_expression_uminus(p):
    """expression : - expression %prec UMINUS"""
    p[0] = -p[2]


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


parser = yacc.yacc()
