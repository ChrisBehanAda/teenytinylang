# Lexer
import sys
import enum

EOF = "\0"


class TokenType(enum.Enum):
    EOF = -1
    NEWLINE = 0
    NUMBER = 1
    IDENT = 2
    STRING = 3
    # Keywords.
    LABEL = 101
    GOTO = 102
    PRINT = 103
    INPUT = 104
    LET = 105
    IF = 106
    THEN = 107
    ENDIF = 108
    WHILE = 109
    REPEAT = 110
    ENDWHILE = 111
    # Operators.
    EQ = 201
    PLUS = 202
    MINUS = 203
    ASTERISK = 204
    SLASH = 205
    EQEQ = 206
    NOTEQ = 207
    LT = 208
    LTEQ = 209
    GT = 210
    GTEQ = 211


class Token:
    def __init__(self, text: str, kind: TokenType):
        self.text = text
        self.kind = kind


class Lexer:
    def __init__(self, source):
        self.source = source + "\n"
        self.cur_char = ""
        self.cur_pos = -1
        self.next_char()

    @staticmethod
    def get_keyword(text) -> TokenType | None:
        for kind in TokenType:
            if text == kind.name and kind.value > 100 and kind.value < 200:
                return kind
        return None

    def next_char(self):
        self.cur_pos += 1
        if self.cur_pos >= len(self.source):
            self.cur_char = EOF
        else:
            self.cur_char = self.source[self.cur_pos]

    def peek(self):
        next_pos = self.cur_pos + 1
        if next_pos >= len(self.source):
            return EOF
        return self.source[next_pos]

    def abort(self, message):
        sys.exit(f"lexing error: {message}")

    def skip_whitespace(self):
        whitespace_chars = [" ", "\t", "\r"]
        while self.cur_char in whitespace_chars:
            self.next_char()

    def skip_comment(self):
        if self.cur_char == "#":
            while self.cur_char != "\n":
                self.next_char()

    def get_token(self) -> Token:
        self.skip_whitespace()
        self.skip_comment()

        token = None
        if self.cur_char == "+":
            token = Token(self.cur_char, TokenType.PLUS)
        elif self.cur_char == "-":
            token = Token(self.cur_char, TokenType.MINUS)
        elif self.cur_char == "*":
            token = Token(self.cur_char, TokenType.ASTERISK)
        elif self.cur_char == "/":
            token = Token(self.cur_char, TokenType.SLASH)
        elif self.cur_char == "\n":
            token = Token(self.cur_char, TokenType.NEWLINE)
        elif self.cur_char == "=":
            if self.peek() == "=":
                prev_char = self.cur_char
                self.next_char()
                token = Token(prev_char + self.cur_char, TokenType.EQEQ)
            else:
                token = Token(self.cur_char, TokenType.EQ)
        elif self.cur_char == ">":
            if self.peek() == "=":
                prev_char = self.cur_char
                self.next_char()
                token = Token(prev_char + self.cur_char, TokenType.GTEQ)
            else:
                token = Token(self.cur_char, TokenType.GT)
        elif self.cur_char == "<":
            if self.peek() == "=":
                prev_char = self.cur_char
                self.next_char()
                token = Token(prev_char + self.cur_char, TokenType.LTEQ)
            else:
                token = Token(self.cur_char, TokenType.LT)
        elif self.cur_char == "!":
            if self.peek() == "=":
                prev_char = self.cur_char
                self.next_char()
                token = Token(prev_char + self.cur_char, TokenType.NOTEQ)
            else:
                self.abort(f"Expected != but got a lone !")
        elif self.cur_char == EOF:
            token = Token("", TokenType.EOF)
        elif self.cur_char == '"':
            self.next_char()
            start_pos = self.cur_pos
            illegal_string_chars = ["\r", "\n", "\t", "\\", "%"]
            while self.cur_char != '"':
                if self.cur_char in illegal_string_chars:
                    self.abort(f"Illegal character in string: {self.cur_char}")
                self.next_char()
            token_text = self.source[start_pos : self.cur_pos]
            token = Token(token_text, TokenType.STRING)
        elif self.cur_char.isdigit():
            start_pos = self.cur_pos
            while self.peek().isdigit():
                self.next_char()
            if self.peek() == ".":
                self.next_char()
                if not self.peek().isdigit():
                    self.abort(f"decimals must be followed by at least one digit")
                while self.peek().isdigit():
                    self.next_char()
            num_str = self.source[start_pos : self.cur_pos]
            token = Token(num_str, TokenType.NUMBER)
        elif self.cur_char.isalpha():
            start_pos = self.cur_pos
            while self.peek().isalpha():
                self.next_char()
            text = self.source[start_pos : self.cur_pos + 1]
            kind = self.get_keyword(text)
            if kind:
                token = Token(text, kind)
            else:
                token = Token(text, TokenType.IDENT)
        else:
            self.abort(f"unknown token: {self.cur_char}")

        self.next_char()
        return token  # type: ignore
