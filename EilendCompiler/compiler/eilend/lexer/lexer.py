import string

from eilend.lexer.token import (
    ALLOWED_ID_CHARS,
    KEYWORDS, SIMPLE_ESCAPE_CHAR_TO_VALUE,
    Token,
    TokenType,
)
from syntactix.lexical.lexer import LexerBase


class Lexer(LexerBase[Token, TokenType]):
    """Eilend lexer."""

    @classmethod
    def make_lexer(cls, src: str):
        return Lexer(src, Token)

    def scan_char(self) -> None:
        ch = self.consume()
        if ch == "\n":
            self.add_token(TokenType.NEWLINE)
            self.mark_next_line()
        elif ch in " \t":
            self.reset_start()
        elif ch == "#":
            self.consume_while(
                lambda: self.peek != "\n",
                not_at_end=True
            )
            self.reset_start()
        elif ch in "()[]{}+%:,&|":
            self.add_token(TokenType(ch))
        elif ch == "-":
            if self.match(">"):
                self.add_token(TokenType.ARROW)
            else:
                self.add_token(TokenType.MINUS)
        elif ch == "*":
            if self.match("*"):
                self.add_token(TokenType.DOUBLE_STAR)
            else:
                self.add_token(TokenType.STAR)
        elif ch == "/":
            if self.match("/"):
                self.add_token(TokenType.INTDIV)
            else:
                self.add_token(TokenType.DIVIDE)
        elif ch == ">":
            if self.match("="):
                self.add_token(TokenType.GTE)
            else:
                self.add_token(TokenType.GT)
        elif ch == "<":
            if self.match("="):
                self.add_token(TokenType.LTE)
            else:
                self.add_token(TokenType.LT)
        elif ch == "!":
            if self.match("="):
                self.add_token(TokenType.NEQ)
            else:
                self.add_token(TokenType.NOT)
        elif ch == "=":
            if self.match("="):
                self.add_token(TokenType.EQ)
            else:
                self.add_token(TokenType.ASSIGN)
        elif ch == "?":
            if self.match("?"):
                self.consume_while(
                    lambda: self.peek in ALLOWED_ID_CHARS,
                    not_at_end=True
                )
                self.add_token(TokenType.NAMED_QUESTION)
            else:
                self.add_token(TokenType.QUESTION)
        elif ch == ".":
            if self.match("."):
                self.add_token(TokenType.RANGE)
            else:
                self.add_token(TokenType.DOT)
        elif ch in '"'"'":
            self.inc_pos(-1)
            self.scan_string()
        elif ch.isnumeric():
            self.inc_pos(-1)
            self.scan_number()
        elif ch in ALLOWED_ID_CHARS:
            self.inc_pos(-1)
            self.scan_id()
        else:
            self.unexpected(ch)

    def scan_string(self) -> None:
        start = self.require(["'", '"'])
        escaping = False
        string = []
        while self.not_at_end and (not escaping <= (self.peek != start)):
            ch = self.consume()
            if ch == "\\" and not escaping:
                escaping = True
                continue
            if escaping:
                if ch in "nrfabtv0":
                    string.append(SIMPLE_ESCAPE_CHAR_TO_VALUE[ch])
                elif ch == "x":
                    string.append(self.scan_ascii_escape())
                elif ch == "u":
                    string.append(self.scan_unicode_escape())
                elif ch in "\\\"":
                    string.append(ch)
                else:
                    self.unexpected(ch)
                escaping = False
            else:
                string.append(ch)
        self.add_token(TokenType.STRING, "".join(string))

    def scan_ascii_escape(self) -> str:
        a = self.require([ch for ch in string.hexdigits])
        b = self.require([ch for ch in string.hexdigits])
        return chr(int(f"{a}{b}", 16))

    def scan_unicode_escape(self) -> str:
        a = self.require([ch for ch in string.hexdigits])
        b = self.require([ch for ch in string.hexdigits])
        c = self.require([ch for ch in string.hexdigits])
        d = self.require([ch for ch in string.hexdigits])
        return chr(int(f"{a}{b}{c}{d}", 16))

    def scan_number(self) -> None:
        number = self.consume_while(
            lambda: self.peek in string.digits,
            not_at_end=True
        )
        if self.match("."):
            if self.peek not in string.digits:
                # Allow something like 1.some_field
                self.inc_pos(-1)
            else:
                frac_part = self.consume_while(
                    lambda: self.peek in string.digits,
                    not_at_end=True
                )
                number += f".{frac_part}"
        self.add_token(TokenType.NUMBER, value=float(number))

    def scan_id(self) -> None:
        ident = self.consume_while(
            lambda: self.peek in ALLOWED_ID_CHARS,
            not_at_end=True
        )
        if ident in KEYWORDS:
            self.add_token(KEYWORDS[ident])
        else:
            self.add_token(TokenType.ID)
