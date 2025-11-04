from eilend.parser.nodes.base import Node, ExprNode
from eilend.parser.nodes.expression import VarNode, FieldAccessNode, IndexNode


def can_be_an_assign_target(node: Node) -> bool:
    return isinstance(node, VarNode | FieldAccessNode | IndexNode)
