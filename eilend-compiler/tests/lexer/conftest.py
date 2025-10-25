from eilend.lexer.lexer import Lexer
from eilend.lexer.token import Token


def call_lexer(src: str) -> list[Token]:
    return Lexer.make_lexer(src).scan()
