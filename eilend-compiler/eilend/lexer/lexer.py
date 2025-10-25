from csv import excel

from syntactix.lexical.lexer import LexerBase
from syntactix.lexical.exceptions import (
    LexerRequireFailedError,
    LexerUnexpectedCharError,
)

from eilend.lexer.token import (
    ALLOWED_NAME_CHARS, ALLOWED_NAME_START_CHARS,
    ESCAPES, KEYWORDS, PUNCTUATION,
    Token,
    TokenType,
)


class Lexer(LexerBase[Token, TokenType]):
    @classmethod
    def make_lexer(cls, src: str):
        return Lexer(src, Token)

    def scan_char(self) -> None:
        ch = self.consume()
        if ch in {"<", ">", "="}:
            if self.match("="):
                self.add_token(TokenType(ch + self.prev))
            else:
                self.add_token(TokenType(ch))
        elif ch == "!":
            self.require("=")
            self.add_token(TokenType.NEQ)
        elif ch == ".":
            if self.match(".."):
                self.add_token(TokenType.VARARG)
            else:
                self.add_token(TokenType.DOT)
        elif ch == "-":
            if self.match(">"):
                self.add_token(TokenType.ARROW)
            else:
                self.add_token(TokenType.MINUS)
        elif ch in PUNCTUATION:
            self.add_token(TokenType(ch))
        elif ch in " \t":
            self.reset_start()
        elif ch in "\r\n":
            self.add_token(TokenType.NEWLINE)
            self.mark_next_line()
            self.reset_start()
        elif ch.isnumeric():
            self.scan_number()
        elif ch == '"':
            self.scan_string()
        elif ch in ALLOWED_NAME_START_CHARS:
            self.scan_name()
        else:
            self.unexpected(ch)

    def scan_number(self) -> None:
        self.consume_while(
            lambda: self.peek.isnumeric(),
            not_at_end=True
        )
        if self.match("."):
            if self.peek.isnumeric():
                self.consume_while(
                    lambda: self.peek.isnumeric(),
                    not_at_end=True
                )
            else:
                # roll back, not a float number
                self.inc_pos(-1)
        self.add_token(TokenType.NUMBER)

    def scan_string(self) -> None:
        escaping = False
        chars = []
        while self.peek and (self.peek != '"' or escaping):
            if self.peek == "\\" and not escaping:
                escaping = True
                self.consume()
                continue
            if escaping:
                if self.peek not in ESCAPES:
                    self.error(
                        LexerRequireFailedError, strings=ESCAPES.keys()
                    )
                chars.append(ESCAPES[self.peek])
                escaping = False
                self.consume()
                continue
            chars.append(self.peek)
            self.consume()
        self.require('"')
        self.add_token(TokenType.STRING, "".join(chars))

    def scan_name(self) -> None:
        name = self.prev + self.consume_while(
            lambda: self.peek in ALLOWED_NAME_CHARS,
            not_at_end=True
        )
        if name in KEYWORDS:
            self.add_token(KEYWORDS[name])
        else:
            self.add_token(TokenType.NAME, name)
