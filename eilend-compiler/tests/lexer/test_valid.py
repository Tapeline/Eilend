from numbers import Number

import pytest
from hypothesis import given
from eilend.lexer.token import Token, TokenType

from tests.lexer.conftest import call_lexer
from tests.lexer.strategies import (
    valid_identifier,
    valid_number_literal,
    valid_string_literal,
)


def test_punctuation():
    tokens = call_lexer(
        "( ) { } [ ] + - * / % < <= > >= == != = -> . : ... ,"
    )
    token_types = [token.type for token in tokens]
    assert token_types == [
        TokenType.LPAREN, TokenType.RPAREN, TokenType.LBRACE,
        TokenType.RBRACE, TokenType.LBRACKET, TokenType.RBRACKET,
        TokenType.PLUS, TokenType.MINUS, TokenType.STAR, TokenType.DIVIDE,
        TokenType.MODULO, TokenType.LESS, TokenType.LESS_EQ,
        TokenType.GREATER, TokenType.GREATER_EQ, TokenType.EQ,
        TokenType.NEQ, TokenType.ASSIGN, TokenType.ARROW, TokenType.DOT,
        TokenType.COLON, TokenType.VARARG, TokenType.COMMA
    ]


@given(src=valid_number_literal())
def test_numbers(src: str):
    tokens = call_lexer(src)
    assert len(tokens) == 1
    assert tokens[0].type == TokenType.NUMBER
    assert tokens[0].lexeme == src


@given(src=valid_string_literal())
def test_strings(src: str):
    tokens = call_lexer(src)
    assert len(tokens) == 1
    assert tokens[0].type == TokenType.STRING
    assert tokens[0].lexeme == src


@given(src=valid_identifier())
def test_names(src: str):
    tokens = call_lexer(src)
    assert len(tokens) == 1
    assert tokens[0].type == TokenType.NAME
    assert tokens[0].lexeme == src
