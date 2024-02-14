# Parser
from lexer import Lexer, TokenType
import sys


class Parser:
    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        self.cur_token = None
        self.peek_token = None
        self.next_token()
        self.next_token()

    def check_token(self, kind):
        return kind == self.cur_token.kind

    def check_peek(self, kind):
        return kind == self.peek_token.kind

    def match(self, kind):
        if not self.check_token(kind):
            self.abort(f"Expected {kind.name} but got {self.cur_token.kind.name}")
        self.next_token()

    def next_token(self):
        self.cur_token = self.peek_token
        self.peek_token = self.lexer.get_token()

    def abort(self, message):
        sys.exit(f"Error: {message}")

    def program(self):
        print("PROGRAM")
        while not self.check_token(TokenType.EOF):
            self.statement()

    def statement(self):
        # "PRINT" (expression | string)
        if self.check_token(TokenType.PRINT):
            print("STATEMENT-PRINT")
            self.next_token()
            if self.check_token(TokenType.STRING):
                self.next_token()
            else:
                self.expression()
        # "IF" comparison "THEN" {statement} "ENDIF"
        elif self.check_token(TokenType.IF):
            print("STATEMENT-IF")
            self.next_token()
            self.comparison()
            self.match(TokenType.THEN)
            self.nl()
            while not self.check_token(TokenType.ENDIF):
                self.statement()
            self.match(TokenType.ENDIF)
        # "WHILE" comparison "REPEAT" {statement} "ENDWHILE"
        elif self.check_token(TokenType.WHILE):
            print("STATEMENT-WHILE")
            self.next_token()
            self.comparison()

            self.match(TokenType.REPEAT)
            self.nl()

            while not self.check_token(TokenType.ENDWHILE):
                self.statement()

            self.match(TokenType.ENDWHILE)

        # "LABEL" ident nl
        elif self.check_token(TokenType.LABEL):
            print("STATEMENT-LABEL")
            self.next_token()
            self.match(TokenType.IDENT)

        # "GOTO" ident nl
        elif self.check_token(TokenType.GOTO):
            print("STATEMENT-LABEL")
            self.next_token()
            self.match(TokenType.IDENT)

        elif self.check_token(TokenType.LET):
            print("STATEMENT-LET")
            self.next_token()
            self.match(TokenType.IDENT)
            self.match(TokenType.EQ)
            self.expression()

        elif self.

        self.nl()

    def nl(self):
        print("NEWLINE")
        self.match(TokenType.NEWLINE)
        while self.check_token(TokenType.NEWLINE):
            self.next_token()

    def expression(self):
        print("EXPRESSION")

    def comparison(self):
        print("COMPARISON")
