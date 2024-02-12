from lexer import Lexer, EOF, TokenType


def main():
    source = "IF+-123 foo*THEN/"
    lexer = Lexer(source)

    token = lexer.get_token()
    while token.kind != TokenType.EOF:
        print(token.kind)
        token = lexer.get_token()


main()
