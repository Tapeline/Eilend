import string
from dataclasses import dataclass
from enum import Enum
from types import MappingProxyType
from typing import Final

from syntactix.lexical.token import TokenLike, TokenPos


class TokenType(Enum):
    LPAREN = "("
    RPAREN = ")"
    LBRACE = "{"
    RBRACE = "}"
    LBRACKET = "["
    RBRACKET = "]"

    PLUS = "+"
    MINUS = "-"
    STAR = "*"
    DIVIDE = "/"
    MODULO = "%"

    NOT = "not"
    LEN = "len"

    LESS = "<"
    LESS_EQ = "<="
    GREATER = ">"
    GREATER_EQ = ">="
    EQ = "=="
    NEQ = "!="

    AND = "and"
    OR = "or"

    ASSIGN = "="
    ARROW = "->"
    DOT = "."
    COLON = ":"
    VARARG = "..."
    COMMA = ","
    LOCAL = "local"
    TYPING = "::"
    TYPE_AND = "&"
    TYPE_OR = "|"
    TYPE_NOT = "~"

    TYPE = "type"
    FUNCTION = "function"
    IF = "if"
    ELSE = "else"
    WHILE = "while"
    FOR = "for"
    IN = "in"
    REPEAT = "repeat"
    UNTIL = "until"
    RETURN = "return"
    BREAK = "break"

    NIL = "nil"
    TRUE = "true"
    FALSE = "false"
    INT = "int"
    FLOAT = "float"
    STRING = "string"
    NAME = "name"

    NEWLINE = "\n"
    COMMENT = "#"


@dataclass(slots=True, frozen=True)
class Token(TokenLike[str, TokenType]):
    type: TokenType
    lexeme: str
    value: str
    pos: TokenPos

    @classmethod
    def eof(cls, pos: TokenPos) -> "Token":
        return Token(TokenType.NEWLINE, "EOF", "EOF", pos)


KEYWORDS: Final = MappingProxyType(
    {
        "function": TokenType.FUNCTION,
        "if": TokenType.IF,
        "else": TokenType.ELSE,
        "while": TokenType.WHILE,
        "for": TokenType.FOR,
        "in": TokenType.IN,
        "repeat": TokenType.REPEAT,
        "until": TokenType.UNTIL,
        "return": TokenType.RETURN,
        "break": TokenType.BREAK,
        "nil": TokenType.NIL,
        "true": TokenType.TRUE,
        "false": TokenType.FALSE,
        "and": TokenType.AND,
        "or": TokenType.OR,
        "not": TokenType.NOT,
        "len": TokenType.LEN,
        "local": TokenType.LOCAL,
    }
)

PUNCTUATION: Final = frozenset(
    (
        "(",
        ")",
        "{",
        "}",
        "[",
        "]",
        "+",
        "-",
        "*",
        "/",
        "%",
        "<",
        "<=",
        ">",
        ">=",
        "==",
        "!=",
        "=",
        "->",
        ".",
        ":",
        "...",
        ",",
        "::",
        "&",
        "|",
        "~"
    )
)

ALLOWED_NAME_START_CHARS: Final = string.ascii_letters + "_"
ALLOWED_NAME_CHARS: Final = string.ascii_letters + string.digits + "_"

ESCAPES: Final = MappingProxyType({
    "n": "\n",
    "r": "\r",
    "t": "\t",
    "a": "\a",
    "b": "\b",
    "f": "\f",
    "v": "\v",
    "\\": "\\",
    '"': '"',
    "\n": "\n",
    "\r": "\r",
})
