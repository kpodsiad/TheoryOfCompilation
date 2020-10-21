#!/usr/bin/python3
import sys
# scanner.py is a file you create, (it is not an external library)
import scanner


if __name__ == '__main__':
    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else 'example.txt'
        file = open(filename, 'r')
    except IOError:
        print(f'Cannot open file: {filename}')
        sys.exit(0)

    text = file.read()
    lexer = scanner.lexer
    lexer.input(text)  # Give the lexer some input

    # Tokenize
    while True:
        tok = lexer.token()
        if tok is None:
            break    # No more input
        column = tok.lexpos - lexer.last_newline
        print(f'({tok.lineno}, {column}): {tok.type}({tok.value})')
