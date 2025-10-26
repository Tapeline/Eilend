import itertools

from eilend.lexer.token import Token
from eilend.parser.constants import BIN_OP_MAP
from eilend.parser.nodes.expression import BinOp, BinOpNode, ExprNode


def desugar_compound_comparison(
    base: ExprNode, cmps: list[tuple[Token, ExprNode]]
) -> ExprNode:
    if not cmps:
        return base
    first_cmp, *other_cmps = cmps
    first_cmp_tok, first_cmp_rhs = first_cmp
    base = BinOpNode(
        first_cmp_tok, base, first_cmp_rhs, BIN_OP_MAP[first_cmp_tok.type]
    )
    for [l_op, l_expr], [r_op, r_expr] in itertools.pairwise(other_cmps):
        base = BinOp(
            l_op,
            base,
            BinOpNode(r_op, l_expr, r_expr, BIN_OP_MAP[r_op.type]),
            BinOp.AND
        )
    return base
