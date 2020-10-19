#!/usr/bin/env python

import sys
import ply.lex as lex

reserved = {
    'if': 'IF',
    'then': 'THEN',
    'else': 'ELSE',
    'while': 'WHILE',
}

tokens = \
    ['ID',
     'Plus',
     'Minus',
     'Multiply',
     'Divide',
     'LeftParen',
     'RightParen',
     'NUMBER',
     'MatBinaryPlus',
     'MatrixBinaryMinus',
     'MatrixBinaryMultiply',
     'MatrixBinaryDivide',
     ] + list(reserved.values())

t_Plus = r'\+'
t_Minus = r'-'
t_Multiply = r'\*'
t_Divide = r'/'
t_LeftParen = r'\('
t_RightParen = r'\)'
t_MatBinaryPlus = r'\.\+'
t_MatrixBinaryMinus = r'\.-'
t_MatrixBinaryMultiply = r'\.\*'
t_MatrixBinaryDivide = r'\./'

t_ignore = ' \t'


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')  # Check for reserved words
    return t


def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print("line %d: illegal character '%s'" % (t.lineno, t.value[0]))
    t.lexer.skip(1)


lexer = lex.lex()
fh = None
try:
    fh = open(sys.argv[1] if len(sys.argv) > 1 else "example.txt", "r")
    lexer.input(fh.read())
    for token in lexer:
        print("line %d: %s(%s)" % (token.lineno, token.type, token.value))
except:
    print("open error\n")
