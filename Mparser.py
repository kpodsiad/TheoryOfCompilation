#!/usr/bin/python

import scanner
import ply.yacc as yacc


tokens = scanner.tokens

precedence = (
    # to fill ...
    ('left', '+', '-', 'DOTADD', 'DOTSUB'),
    ('left', '*', '/', 'DOTMUL', 'DOTDIV'),
    ('right', 'UMINUS'),
    ('left', 'TRANSPOSITION'),
    ('left', 'GE', 'LE', 'LT', 'GT', 'EQ', 'NE'), # to nie powinno być nonassoc? teraz chyba można robić a < b < ... < z
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
    """expression : '-' expression %prec UMINUS"""
    p[0] = '-' + p[2]  # inaczej python pluł się, że operator - jest używany ze złym typem


def p_expression_transposition(p):
    """expression : expression TRANSPOSITION"""
    p[0] = p[2] + "'"


def p_expression_trivial(p):
    """expression : number
                  | ID"""
    p[0] = p[1]


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
