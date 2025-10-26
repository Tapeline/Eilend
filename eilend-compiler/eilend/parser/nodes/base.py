from dataclasses import dataclass
from typing import Protocol, final

from syntactix.parser.nodes import NodeLike

from eilend.lexer.token import Token


class Node(NodeLike[Token]):
    token: Token


class ExprNode(Node):
    """Narrows down to expressions."""


@final
class NameQualifierItemAccess:
    DOT = "."
    COLON = ":"


@dataclass(frozen=True, slots=True)
class NameQualifierItem:
    name: str
    access: NameQualifierItemAccess


@dataclass(frozen=True, slots=True)
class QualName:
    token: Token
    base_name: str
    qualifiers: list[NameQualifierItem]
