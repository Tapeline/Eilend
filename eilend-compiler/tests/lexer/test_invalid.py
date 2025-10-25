import pytest
from hypothesis import given, example
from syntactix.lexical.exceptions import LexerError, LexerUnexpectedCharError

from tests.lexer.conftest import call_lexer


@pytest.mark.parametrize(
    "src",
    "@~`$;^&?'\\|"
)
def test_unexpected_char(src):
    with pytest.raises(LexerUnexpectedCharError):
        call_lexer(src)


@pytest.mark.parametrize(
    "src",
    ["1_0", "1e4", "1abcd"]
)
def test_numbers(src: str):
    with pytest.raises(LexerError):
        call_lexer(src)


@pytest.mark.parametrize(
    "src",
    ['"', '"\\"', '"\n"', '"\r"']
)
def test_strings(src: str):
    with pytest.raises(LexerError):
        call_lexer(src)
