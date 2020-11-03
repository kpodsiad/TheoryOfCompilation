from ply.lex import lex, Lexer


reserved = {
    'if': 'IF', 'else': 'ELSE', 'while': 'WHILE',
    'break': 'BREAK', 'continue': 'CONTINUE', 'return': 'RETURN',
    'eye': 'EYE', 'zeros': 'ZEROS', 'ones': 'ONES', 'print': 'PRINT'
}


tokens = (
    'DOTADD', 'DOTSUB', 'DOTMUL', 'DOTDIV', 'ADDASSIGN', 'SUBASSIGN',
    'MULASSIGN', 'DIVASSIGN', 'LE', 'GE', 'EQ', 'NE', 'ID', 'INT',
    'FLOAT', 'STR'
) + tuple(reserved.values())


t_DOTADD = r'\.\+'
t_DOTSUB = r'\.-'
t_DOTMUL = r'\.\*'
t_DOTDIV = r'\./'
t_ADDASSIGN = r'\+='
t_SUBASSIGN = r'-='
t_MULASSIGN = r'\*='
t_DIVASSIGN = r'/='
t_LE = r'<='
t_GE = r'>='
t_EQ = r'=='
t_NE = r'\!='

literals = "+-*/=()[]{}<>:',;"
t_ignore = ' \t'
t_ignore_COMMENT = r'\#.*'


def t_FLOAT(t):
    r'(((\d+\.\d*)|(\.\d+))(([eE]\d+)?)|(\d+(.\d*)?[eE]\d+))'
    t.value = float(t.value)
    return t


def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_STR(t):
    r'"([^"]|\\")*"'
    t.value = t.value[1:-1]
    return t


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')    # Check for reserved words
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    t.lexer.last_newline = t.lexpos + len(t.value) - 1


def t_error(t):
    column = find_tok_column(t)
    print(
        f"Illegal character at line {t.lineno} column {column}: '{t.value[0]}'")
    t.lexer.skip(1)


def find_tok_column(t):
    return t.lexpos - t.lexer.last_newline

lexer = lex()
lexer.last_newline = -1
