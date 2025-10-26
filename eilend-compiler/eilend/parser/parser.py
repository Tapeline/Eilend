from types import MappingProxyType
from typing import Final

from syntactix.parser.parser import ParserBase
from syntactix.parser.exceptions import ParserRequireFailedError

from eilend.lexer.token import Token, TokenType
from eilend.parser.constants import BIN_OP_MAP, UN_OP_MAP
from eilend.parser.desugar import desugar_compound_comparison
from eilend.parser.exceptions import AssignListLenDiffersError, BadNumberError
from eilend.parser.nodes.base import (
    Node, QualName, NameQualifierItem,
    NameQualifierItemAccess,
)
from eilend.parser.nodes.control import (
    WhileNode, IfNode, ForNode,
    ForEachNode, RepeatUntilNode,
    ElseIfClause, ReturnNode, BreakNode,
)
from eilend.parser.nodes.expression import (
    ExprNode, UnOpNode, VarNode, CallNode, LambdaNode, BinOpNode, IndexNode,
    TableNode, BinOp, FieldAccessNode, UnOp, LiteralInt, LiteralNil,
    LiteralStr, LiteralBool, LiteralFloat, MethCallNode,
)
from eilend.parser.nodes.stmt import (
    BlockNode, FuncDefNode, LocalFuncDefNode,
    LocalDefNode, LocalAssignNode, AssignNode,
)




class Parser(ParserBase[Token, TokenType, Node]):
    def match_skip_line(self, *token_types: TokenType | str) -> Token | None:
        delta = 0
        while self.match(TokenType.NEWLINE):
            delta += 1
        if tok := self.match(*token_types):
            return tok
        else:
            self.inc_pos(-delta)
            return None

    def require_skip_line(self, *types: TokenType | str) -> Token:
        if (token := self.match_skip_line(*types)) is None:
            self.error(ParserRequireFailedError, tokens=types)
        return token

    def parse(self) -> list[Node]:
        nodes = []
        while self.not_at_end:
            nodes.append(self._parse_stmt())
        return nodes

    def _parse_stmt(self) -> Node:
        if block_start := self.match(TokenType.LBRACE):
            nodes = []
            while self.not_at_end and self.peek_rq.type != TokenType.RBRACE:
                nodes.append(self._parse_stmt())
                while self.match(TokenType.NEWLINE):
                    pass  # consume all newlines
            self.require_skip_line(TokenType.RBRACE)
            return BlockNode(block_start, nodes)
        if while_tok := self.match(TokenType.WHILE):
            condition = self._parse_expr()
            body = _block_if_needed(self._parse_stmt())
            return WhileNode(while_tok, condition, body)
        if for_tok := self.match(TokenType.FOR):
            name = self.require(TokenType.NAME)
            if self.match(TokenType.IN):
                expr = self._parse_expr()
                body = _block_if_needed(self._parse_stmt())
                return ForEachNode(for_tok, name, expr, body)
            else:
                self.require(TokenType.ASSIGN)
                start = self._parse_expr()
                self.require(TokenType.COMMA)
                end = self._parse_expr()
                step: ExprNode | None = None
                if self.match_pattern(TokenType.COMMA, "step"):
                    self.require(TokenType.COMMA)
                    self.require("step")
                    step = self._parse_expr()
                body = _block_if_needed(self._parse_stmt())
                return ForNode(for_tok, name, start, end, step, body)
        if repeat_tok := self.match(TokenType.REPEAT):
            body = _block_if_needed(self._parse_stmt())
            self.require(TokenType.UNTIL)
            expr = self._parse_expr()
            return RepeatUntilNode(repeat_tok, expr, body)
        if if_tok := self.match(TokenType.IF):
            if_cond = self._parse_expr()
            if_body = _block_if_needed(self._parse_stmt())
            else_ifs = []
            else_body: BlockNode | None = None
            while self.match_pattern(TokenType.ELSE, TokenType.IF):
                clause_cond = self._parse_expr()
                clause_body = _block_if_needed(self._parse_stmt())
                else_ifs.append(ElseIfClause(clause_cond, clause_body))
            if self.match(TokenType.ELSE):
                else_body = _block_if_needed(self._parse_stmt())
            return IfNode(if_tok, if_cond, if_body, else_ifs, else_body)
        if func_tok := self.match(TokenType.FUNCTION):
            qualname = self._parse_qualname()
            self.require(TokenType.LPAREN)
            params = []
            while self.not_at_end and self.peek_rq.type != TokenType.RPAREN:
                params.append(self.require_skip_line(TokenType.NAME).lexeme)
                if not self.match_skip_line(TokenType.COMMA):
                    break
            self.require_skip_line(TokenType.RPAREN)
            body = _block_if_needed(self._parse_stmt())
            return FuncDefNode(func_tok, qualname, params, body)
        if local_func_toks := self.match_pattern(
            TokenType.LOCAL, TokenType.FUNCTION
        ):
            name = self.require(TokenType.NAME).lexeme
            params = []
            while self.not_at_end and self.peek_rq.type != TokenType.RPAREN:
                params.append(self.require_skip_line(TokenType.NAME).lexeme)
                if not self.match_skip_line(TokenType.COMMA):
                    break
            self.require_skip_line(TokenType.RPAREN)
            body = _block_if_needed(self._parse_stmt())
            return LocalFuncDefNode(local_func_toks[1], name, params, body)
        if local_tok := self.match(TokenType.LOCAL):
            names = [self.require(TokenType.NAME).lexeme]
            while self.match(TokenType.COMMA):
                names.append(self.require(TokenType.NAME).lexeme)
            if assign_tok := self.match(TokenType.ASSIGN):
                exprs = [self._parse_expr()]
                while self.match(TokenType.COMMA):
                    names.append(self._parse_expr())
                if len(names) != len(exprs):
                    self.error(
                        AssignListLenDiffersError,
                        lhs=len(names), rhs=len(exprs)
                    )
                return LocalAssignNode(assign_tok, list(zip(names, exprs)))
            else:
                return LocalDefNode(local_tok, names)
        if return_tok := self.match(TokenType.RETURN):
            expr: ExprNode | None = None
            if self.peek and self.peek.type != TokenType.NEWLINE:
                expr = self._parse_expr()
            return ReturnNode(return_tok, expr)
        if break_tok := self.match(TokenType.BREAK):
            return BreakNode(break_tok)
        return self._parse_expr_or_assign()

    def _parse_expr_or_assign(self) -> Node:
        expr = self._parse_expr()
        targets = [expr]
        if assign_tok := self.match(TokenType.ASSIGN):
            expr = self._parse_expr()
            return AssignNode(assign_tok, [(targets[0], expr)])
        if not self.match(TokenType.COMMA):
            return expr
        while self.match(TokenType.COMMA):
            targets.append(self._parse_expr())
        assign_tok = self.require(TokenType.ASSIGN)
        exprs = [self._parse_expr()]
        while self.match(TokenType.COMMA):
            exprs.append(self._parse_expr())
        if len(targets) != len(exprs):
            self.error(
                AssignListLenDiffersError,
                lhs=len(targets), rhs=len(exprs)
            )
        return AssignNode(assign_tok, list(zip(targets, exprs)))

    def _parse_qualname(self) -> QualName:
        base_tok = self.require(TokenType.NAME)
        qualifiers = []
        while self.match_skip_line(TokenType.DOT):
            qualifiers.append(
                NameQualifierItem(
                    self.require(TokenType.NAME).lexeme,
                    NameQualifierItemAccess.DOT
                )
            )
        if self.match_skip_line(TokenType.COLON):
            qualifiers.append(
                NameQualifierItem(
                    self.require(TokenType.NAME).lexeme,
                    NameQualifierItemAccess.COLON
                )
            )
        return QualName(base_tok, base_tok.lexeme, qualifiers)

    def _parse_expr(self) -> ExprNode:
        return self._parse_or()

    def _parse_or(self) -> ExprNode:
        lhs = self._parse_and()
        while tok := self.match(TokenType.OR):
            rhs = self._parse_and()
            lhs = BinOpNode(tok, lhs, rhs, BinOp.OR)
        return lhs

    def _parse_and(self) -> ExprNode:
        lhs = self._parse_cmp()
        while tok := self.match_skip_line(TokenType.AND):
            rhs = self._parse_cmp()
            lhs = BinOpNode(tok, lhs, rhs, BinOp.AND)
        return lhs

    def _parse_cmp(self) -> ExprNode:
        lhs = self._parse_term()
        additional: list[tuple[Token, ExprNode]] = []
        while tok := self.match_skip_line(
            TokenType.LESS,
            TokenType.GREATER,
            TokenType.LESS_EQ,
            TokenType.GREATER_EQ,
            TokenType.EQ,
            TokenType.NEQ
        ):
            rhs = self._parse_term()
            additional.append((tok, rhs))
        return desugar_compound_comparison(lhs, additional)

    def _parse_term(self) -> ExprNode:
        lhs = self._parse_factor()
        while tok := self.match_skip_line(
            TokenType.PLUS, TokenType.MINUS
        ):
            rhs = self._parse_factor()
            lhs = BinOpNode(tok, lhs, rhs, BIN_OP_MAP[tok.type])
        return lhs

    def _parse_factor(self) -> ExprNode:
        lhs = self._parse_unary()
        while tok := self.match_skip_line(
            TokenType.STAR, TokenType.DIVIDE, TokenType.MODULO
        ):
            rhs = self._parse_unary()
            lhs = BinOpNode(tok, lhs, rhs, BIN_OP_MAP[tok.type])
        return lhs

    def _parse_unary(self) -> ExprNode:
        if tok := self.match_skip_line(
            TokenType.MINUS, TokenType.LEN, TokenType.NOT
        ):
            return UnOpNode(tok, self._parse_unary(), UN_OP_MAP[tok.type])
        return self._parse_call()

    def _parse_call(self) -> ExprNode:
        expr = self._parse_primary()
        while True:
            if call_tok := self.match_skip_line(TokenType.LPAREN):
                args = [self._parse_expr()]
                while self.match_skip_line(TokenType.COMMA):
                    args.append(self._parse_expr())
                self.require_skip_line(TokenType.RPAREN)
                expr = CallNode(call_tok, expr, args)
            elif meth_tok := self.match_skip_line(TokenType.COLON):
                meth_name = self.require(TokenType.NAME)
                self.require(TokenType.LPAREN)
                args = [self._parse_expr()]
                while self.match_skip_line(TokenType.COMMA):
                    args.append(self._parse_expr())
                self.require_skip_line(TokenType.RPAREN)
                expr = MethCallNode(meth_tok, meth_name, expr, args)
            elif dot_tok := self.match_skip_line(TokenType.DOT):
                name = self.require(TokenType.NAME)
                expr = FieldAccessNode(dot_tok, expr, name)
            elif index_tok := self.match(TokenType.LBRACKET):
                index = self._parse_expr()
                self.require_skip_line(TokenType.RBRACKET)
                expr = IndexNode(index_tok, expr, index)
            elif tok := self.peek and self.peek.type == TokenType.RBRACE:
                table = self._parse_table()
                expr = CallNode(tok, expr, [table])
            elif tok := self.match(TokenType.STRING):
                expr = CallNode(tok, expr, [LiteralStr(tok, tok.value)])
            else:
                break
        return expr

    def _parse_primary(self) -> ExprNode:
        if tok := self.match(TokenType.NIL):
            return LiteralNil(tok)
        if tok := self.match(TokenType.INT):
            try:
                return LiteralInt(tok, int(tok.value))
            except ValueError:
                self.error(BadNumberError, number=tok.value)
        if tok := self.match(TokenType.FLOAT):
            try:
                return LiteralFloat(tok, float(tok.value))
            except ValueError:
                self.error(BadNumberError, number=tok.value)
        if tok := self.match(TokenType.STRING):
            return LiteralStr(tok, tok.value)
        if tok := self.match(TokenType.LPAREN):
            params = []
            initial = self.i
            can_be_lambda = True
            while self.not_at_end and self.peek_rq.type != TokenType.RPAREN:
                name_tok = self.match_skip_line(TokenType.NAME)
                if not name_tok:
                    can_be_lambda = False
                    break
                params.append(name_tok.lexeme)
                if not self.match_skip_line(TokenType.COMMA):
                    break
            if can_be_lambda:
                self.require_skip_line(TokenType.RPAREN)
                arrow = self.require(TokenType.ARROW)
                body = _block_if_needed(self._parse_stmt())
                return LambdaNode(arrow, params, body)
            else:
                self.i = initial  # reset
                # consume newlines
                while self.match(TokenType.NEWLINE):
                    pass
                expr = self._parse_expr()
                self.require_skip_line(TokenType.RPAREN)
                return expr
        if tok := self.match(TokenType.NAME, TokenType.VARARG):
            if arrow := self.match(TokenType.ARROW):
                body = _block_if_needed(self._parse_stmt())
                return LambdaNode(arrow, [tok.value], body)
            else:
                return VarNode(tok, tok.value)
        if tok := self.match(TokenType.ARROW):
            body = _block_if_needed(self._parse_stmt())
            return LambdaNode(tok, [], body)
        if tok := self.peek and self.peek.type == TokenType.RBRACE:
            return self._parse_table()
        if self.not_at_end:
            self.unexpected(self.peek)
        else:
            self.unexpected(Token.eof(self.pos))

    def _parse_table(self) -> TableNode:
        tok = self.require(TokenType.LBRACE)
        fields = []
        if self.match_skip_line(TokenType.RBRACE):
            return TableNode(tok, fields)
        fields.append(self._parse_table_field())
        while self.match_skip_line(TokenType.COMMA):
            if self.match_skip_line(TokenType.RBRACE):
                break
            fields.append(self._parse_table_field())
        return TableNode(tok, fields)

    def _parse_table_field(self) -> tuple[ExprNode | None, ExprNode]:
        if self.match_skip_line(TokenType.LBRACKET):
            key = self._parse_expr()
            self.require_skip_line(TokenType.RBRACKET)
            self.require_skip_line(TokenType.ASSIGN)
            value = self._parse_expr()
            return key, value
        if key := self.match_skip_line(TokenType.NAME):
            self.require_skip_line(TokenType.ASSIGN)
            value = self._parse_expr()
            return LiteralStr(key, key.lexeme), value
        return None, self._parse_expr()


def _block_if_needed(node: Node) -> BlockNode:
    if isinstance(node, BlockNode):
        return node
    else:
        return BlockNode(node.token, [node])


def remove_comments(tokens: list[Token]) -> list[Token]:
    return [token for token in tokens if token.type != TokenType.COMMENT]


def parse_tokens(tokens: list[Token]) -> list[Node]:
    parser = Parser(tokens)
    return parser.parse()
