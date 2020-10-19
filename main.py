import sys
import ply.lex as lex
# scanner.py is a file you create, (it is not an external library)
import scanner


if __name__ == '__main__':
    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "example.txt"
        file = open(filename, "r")
    except IOError:
        print("Cannot open file: {0}".format(filename))
        sys.exit(0)

    text = file.read()
    lexer = scanner.lexer
    lexer.input(text)  # Give the lexer some input

    # Tokenize
    while True:
        tok = lexer.token()
        if tok is None:
            break    # No more input
        #column = scanner.find_column(text,tok)
        print("({0:d}): {1}({2})".format(tok.lineno, tok.type, tok.value))
