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
     'FloatingPointNumber',
     'IntegerNumber',
     'String',
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
     # assign operators
     'Assign',
     'AddAndAssign',
     'SubtractAndAssign',
     'MultiplyAndAssign',
     'DivideAndAssign',
     # relational operators
     'LesserThan',
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
     # various lexems
     'RangeOperator',
     'MatrixTransposition',
     'Comma',
     'Semicolon',
     'Comment'
     ] + list(reserved.values())


t_String = r'".*"'
# binary operators
t_Plus = r'\+'
t_Minus = r'-'
t_Multiply = r'\*'
t_Divide = r'/'
# matrix binary operators
t_MatBinaryPlus = r'\.\+'
t_MatrixBinaryMinus = r'\.-'
t_MatrixBinaryMultiply = r'\.\*'
t_MatrixBinaryDivide = r'\./'
# assign operators
t_Assign = r'='
t_AddAndAssign = r'\+='
t_SubtractAndAssign = r'-='
t_MultiplyAndAssign = r'\*='
t_DivideAndAssign = r'/='
# relational operators
t_LesserThan = r'<'
t_GreaterThan = r'>'
t_LesserOrEqualThan = r'<='
t_GreaterOrEqualThan = r'>='
t_NotEqual = r'!='
t_Equal = r'=='
# brackets
t_RoundBracketLeft = r'\('
t_RoundBracketRight = r'\)'
t_CurlyBracketLeft = r'\{'
t_CurlyBracketRight = r'\}'
t_SquareBracketLeft = r'\['
t_SquareBracketRight = r'\]'
# various lexems
t_RangeOperator = r':'
t_MatrixTransposition = r"'"
t_Comma = r','
t_Semicolon = r';'
t_ignore_Comment = r'\#.*'

t_ignore = ' \t'


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')  # Check for reserved words
    return t


# it's must be before t_IntegerNumber, otherwise lexer would interpret e.g. 60. like integer(60) and invalid symbol (.)
def t_FloatingPointNumber(t):
    r'(\d*\.\d+)|(\d+\.\d*)' # a.x or x.a where a could be empty
    t.value = float(t.value)
    return t


def t_IntegerNumber(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print("(%d, %d): illegal character '%s'" % (t.lineno, find_column(t), t.value[0]))
    t.lexer.skip(1)


lexer = lex.lex()
source = ""


# Compute column.
# input is the input text string
# token is a token instance
def find_column(token_to_find):
    last_cr = source.rfind('\n', 0, token_to_find.lexpos)
    if last_cr < 0:
        last_cr = 0
    column = (token_to_find.lexpos - last_cr)
    return column
