from dataclasses import dataclass
from enum import Enum
from typing import final

from eilend.lexer.token import Token
from eilend.parser.nodes.base import ExprNode
from eilend.parser.nodes.stmt import BlockNode


@final
class BinOp(Enum):
    ADD = "+"
    SUB = "-"
    MUL = "*"
    DIV = "/"
    MOD = "%"
    LESS = "<"
    LESS_EQ = "<="
    GREATER = ">"
    GREATER_EQ = ">="
    EQ = "=="
    NEQ = "!="
    AND = "and"
    OR = "or"


@dataclass(frozen=True, slots=True)
class BinOpNode(ExprNode):
    token: Token
    l: ExprNode
    r: ExprNode
    op: BinOp


@final
class UnOp(Enum):
    NOT = "not"
    LEN = "len"
    NEG = "neg"


@dataclass(frozen=True, slots=True)
class UnOpNode(ExprNode):
    token: Token
    expr: ExprNode
    op: UnOp


@dataclass(frozen=True, slots=True)
class LiteralNil(ExprNode):
    token: Token


@dataclass(frozen=True, slots=True)
class LiteralBool(ExprNode):
    token: Token
    value: bool


@dataclass(frozen=True, slots=True)
class LiteralInt(ExprNode):
    token: Token
    value: int


@dataclass(frozen=True, slots=True)
class LiteralFloat(ExprNode):
    token: Token
    value: float


@dataclass(frozen=True, slots=True)
class LiteralStr(ExprNode):
    token: Token
    value: str


@dataclass(frozen=True, slots=True)
class VarNode(ExprNode):
    token: Token
    name: str


@dataclass(frozen=True, slots=True)
class LambdaNode(ExprNode):
    token: Token
    args: list[str]
    body: BlockNode


@dataclass(frozen=True, slots=True)
class FieldAccessNode(ExprNode):
    token: Token
    parent: ExprNode
    field: str


@dataclass(frozen=True, slots=True)
class IndexNode(ExprNode):
    token: Token
    parent: ExprNode
    index: ExprNode


@dataclass(frozen=True, slots=True)
class MethCallNode(ExprNode):
    token: Token
    callee: ExprNode
    method: str
    args: list[ExprNode]


@dataclass(frozen=True, slots=True)
class CallNode(ExprNode):
    token: Token
    callee: ExprNode
    args: list[ExprNode]


@dataclass(frozen=True, slots=True)
class TableNode(ExprNode):
    token: Token
    pairs: list[tuple[ExprNode | None, ExprNode]]
