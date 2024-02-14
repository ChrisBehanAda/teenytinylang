from lexer import Lexer, EOF, TokenType
from parse import Parser


def main():
    with open("input.txt", "r") as fp:
        source = fp.read()

    lexer = Lexer(source)
    parser = Parser(lexer)
    parser.program()
    print("Parsing completed.")


main()
