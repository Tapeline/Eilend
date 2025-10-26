from types import MappingProxyType
from typing import Final

from eilend.lexer.token import TokenType
from eilend.parser.nodes.expression import UnOp, BinOp

UN_OP_MAP: Final = MappingProxyType(
    {
        TokenType.MINUS: UnOp.NEG,
        TokenType.NOT: UnOp.NOT,
        TokenType.LEN: UnOp.LEN,
    }
)

BIN_OP_MAP: Final = MappingProxyType(
    {
        TokenType.LESS: BinOp.LESS,
        TokenType.LESS_EQ: BinOp.LESS_EQ,
        TokenType.GREATER: BinOp.GREATER,
        TokenType.GREATER_EQ: BinOp.GREATER_EQ,
        TokenType.EQ: BinOp.EQ,
        TokenType.NEQ: BinOp.NEQ,
        TokenType.OR: BinOp.OR,
        TokenType.AND: BinOp.AND,
        TokenType.PLUS: BinOp.ADD,
        TokenType.MINUS: BinOp.SUB,
        TokenType.STAR: BinOp.MUL,
        TokenType.DIVIDE: BinOp.DIV,
    }
)
