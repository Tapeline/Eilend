from dataclasses import dataclass

from eilend.lexer.token import Token
from eilend.parser.nodes.base import Node, QualName
from eilend.parser.nodes.expression import ExprNode


@dataclass(frozen=True, slots=True)
class BlockNode(Node):
    token: Token
    nodes: list[Node]


@dataclass(frozen=True, slots=True)
class FuncDefNode(Node):
    token: Token
    qualname: QualName
    args: list[str]
    body: BlockNode


@dataclass(frozen=True, slots=True)
class LocalFuncDefNode(Node):
    token: Token
    name: str
    args: list[str]
    body: BlockNode


@dataclass(frozen=True, slots=True)
class AssignNode(Node):
    token: Token
    assigns: list[tuple[ExprNode, ExprNode]]


@dataclass(frozen=True, slots=True)
class LocalDefNode(Node):
    token: Token
    names: list[str]


@dataclass(frozen=True, slots=True)
class LocalAssignNode(Node):
    token: Token
    assigns: list[tuple[str, ExprNode]]
