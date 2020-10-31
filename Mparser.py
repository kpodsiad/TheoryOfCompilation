#!/usr/bin/python

import scanner
import ply.yacc as yacc


tokens = scanner.tokens

precedence = (
    # to fill ...
    ('left', '+', '-', 'DOTADD', 'DOTSUB'),
    ('left', '*', '/')
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
                   | generic_expression
                   | flow_control"""


def p_code_block(p):
    """code_block : { instructions_opt }"""


def p_generic_expression(p):
    """generic_expression : assignment
                          | expression
                          | func_call"""


def p_assignment(p):
    """assignment : ID = generic_expression
                  | ID ADDASSIGN generic_expression
                  | ID SUBASSIGN generic_expression
                  | ID MULASSIGN generic_expression
                  | ID DIVASSIGN generic_expression"""



parser = yacc.yacc()
