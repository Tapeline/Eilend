import string
from dataclasses import dataclass
from enum import Enum
from types import MappingProxyType

from syntactix.lexical.token import TokenLike, TokenPos


class TokenType(Enum):
    L_PAR = "("
    R_PAR = ")"
    L_BRACKET = "["
    R_BRACKET = "]"
    L_BRACE = "{"
    R_BRACE = "}"
    NEWLINE = "newline"

    PLUS = "+"
    MINUS = "-"
    STAR = "*"
    DOUBLE_STAR = "**"
    DIVIDE = "/"
    PERCENT = "%"
    INTDIV = "//"
    COLON = ":"
    COMMA = ","
    ASSIGN = "="
    EQ = "=="
    NEQ = "!="
    GT = ">"
    GTE = ">="
    LT = "<"
    LTE = "<="
    ARROW = "->"
    AMPERSAND = "&"
    PILLAR = "|"
    QUESTION = "?"
    NAMED_QUESTION = "??"
    RANGE = ".."
    DOT = "."
    NOT = "!"

    STRING = "str"
    NUMBER = "num"
    ID = "id"

    TRUE = "true"
    FALSE = "false"
    NULL = "null"

    DEF = "def"
    RETURN = "return"
    THROW = "throw"
    AND = "and"
    OR = "or"
    TRY = "try"
    MATCH = "match"
    CASE = "case"
    IF = "if"
    ELSE = "else"
    WHILE = "while"
    FOR = "for"
    STRUCT = "struct"
    CONSTRUCT = "construct"
    RECORD = "record"
    INTERFACE = "interface"
    IMPORT = "import"
    EXPORT = "export"


KEYWORDS: MappingProxyType = MappingProxyType({
    "def": TokenType.DEF,
    "return": TokenType.RETURN,
    "throw": TokenType.THROW,
    "and": TokenType.AND,
    "or": TokenType.OR,
    "try": TokenType.TRY,
    "match": TokenType.MATCH,
    "case": TokenType.CASE,
    "if": TokenType.IF,
    "else": TokenType.ELSE,
    "while": TokenType.WHILE,
    "for": TokenType.FOR,
    "struct": TokenType.STRUCT,
    "construct": TokenType.CONSTRUCT,
    "record": TokenType.RECORD,
    "interface": TokenType.INTERFACE,
    "import": TokenType.IMPORT,
    "export": TokenType.EXPORT,
    "true": TokenType.TRUE,
    "false": TokenType.FALSE,
    "null": TokenType.NULL
})

ALLOWED_ID_CHARS = string.ascii_letters + string.digits + "_"
SIMPLE_ESCAPE_CHAR_TO_VALUE = {
    "n": "\n",
    "f": "\f",
    "a": "\a",
    "b": "\b",
    "r": "\r",
    "t": "\t",
    "v": "\v",
    "0": "\0"
}


@dataclass
class Token(TokenLike[str | float, TokenType]):  # type: ignore
    type: TokenType
    lexeme: str
    value: str | float
    pos: TokenPos

    def __repr__(self) -> str:
        return f"{self.type.name}: {repr(self.lexeme)}"
