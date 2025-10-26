from dataclasses import dataclass, field

from eilend.lexer.token import Token
from eilend.parser.nodes.base import Node
from eilend.parser.nodes.expression import ExprNode
from eilend.parser.nodes.stmt import BlockNode


@dataclass(frozen=True, slots=True)
class ElseIfClause:
    condition: ExprNode
    body: BlockNode


@dataclass(frozen=True, slots=True)
class IfNode(Node):
    token: Token
    condition: ExprNode
    if_body: BlockNode
    else_if: list[ElseIfClause] = field(default_factory=list)
    else_body: BlockNode | None = None


@dataclass(frozen=True, slots=True)
class WhileNode(Node):
    token: Token
    condition: ExprNode
    body: BlockNode


@dataclass(frozen=True, slots=True)
class ForNode(Node):
    token: Token
    var: str
    start: ExprNode
    end: ExprNode
    step: ExprNode | None
    body: BlockNode


@dataclass(frozen=True, slots=True)
class ForEachNode(Node):
    token: Token
    var: str
    collection: ExprNode
    body: BlockNode


@dataclass(frozen=True, slots=True)
class RepeatUntilNode(Node):
    token: Token
    condition: ExprNode
    body: BlockNode


@dataclass(frozen=True, slots=True)
class ReturnNode(Node):
    token: Token
    expr: ExprNode | None


@dataclass(frozen=True, slots=True)
class BreakNode(Node):
    token: Token
