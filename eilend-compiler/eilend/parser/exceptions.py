from dataclasses import dataclass
from typing import override

from syntactix.lexical.token import TokenPos
from syntactix.parser.exceptions import ParserError


@dataclass
class AssignListLenDiffersError(ParserError):
    pos: TokenPos
    lhs: int
    rhs: int

    @override
    def __str__(self) -> str:
        return (
            f"Assign targets count differs from right-hand side: \n"
            f"{self.lhs} targets = {self.rhs} expressions."
        )


@dataclass
class BadNumberError(ParserError):
    pos: TokenPos
    number: str

    @override
    def __str__(self) -> str:
        return f"Could not parse number {self.number}"
