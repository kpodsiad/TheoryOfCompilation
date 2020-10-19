#!/usr/bin/env python

import ply.lex as lex

reserved = {
    'if': 'IF',
    'then': 'THEN',
    'else': 'ELSE',
    'while': 'WHILE',
}

tokens = \
    ['ID',
     'Number',
     # binary operators
     'Plus',
     'Minus',
     'Multiply',
     'Divide',
     # matrix binary operators
     'MatBinaryPlus',
     'MatrixBinaryMinus',
     'MatrixBinaryMultiply',
     'MatrixBinaryDivide',
     # todo implement following lexems
     # assign operators
     'Assign',
     'AddAndAssign',
     'SubtractAndAssign',
     'MultiplyAndAssign',
     'DivideAndAssign',
     # relational operators
     'LesserThan'
     'GreaterThan',
     'LesserOrEqualThan',
     'GreaterOrEqualThan',
     'NotEqual',
     'Equal',
     # brackets
     'RoundBracketLeft',
     'RoundBracketRight',
     'CurlyBracketLeft',
     'CurlyBracketRight',
     'SquareBracketLeft',
     'SquareBracketRight',
     # various elxems
     'RangeOperator',
     'MatrixTransposition',
     'Comma',
     'Semicolon'
     ] + list(reserved.values())

t_Plus = r'\+'
t_Minus = r'-'
t_Multiply = r'\*'
t_Divide = r'/'

t_MatBinaryPlus = r'\.\+'
t_MatrixBinaryMinus = r'\.-'
t_MatrixBinaryMultiply = r'\.\*'
t_MatrixBinaryDivide = r'\./'

# todo implement
t_LesserThan = r''
t_GreaterThan = r''
t_LesserOrEqualThan = r''
t_GreaterOrEqualThan = r''
t_NotEqual = r''
t_Equal = r''

t_RoundBracketLeft = r'\('
t_RoundBracketRight = r'\)'

t_ignore = ' \t'


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')  # Check for reserved words
    return t


def t_Number(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print("line %d: illegal character '%s'" % (t.lineno, t.value[0]))
    t.lexer.skip(1)


# Compute column.
# input is the input text string
# token is a token instance
def find_column(source: str, token_to_find):
    last_cr = source.rfind('\n', 0, token_to_find.lexpos)
    if last_cr < 0:
        last_cr = 0
    column = (token_to_find.lexpos - last_cr) + 1
    return column


lexer = lex.lex()

# fh = None
# try:
#     fh = open(sys.argv[1] if len(sys.argv) > 1 else "example.txt", "r")
#     lexer.input(fh.read())
#     for token in lexer:
#         print("line %d: %s(%s)" % (token.lineno, token.type, token.value))
# except:
#     print("open error\n")
