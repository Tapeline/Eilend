import os
import sys
from pathlib import Path

from eilend.lexer.lexer import Lexer
from syntactix.error_formatter import format_exception
from syntactix.lexical.exceptions import LexerError
from syntactix.lexical.lexer import make_lexer


def main():
    filename = "../test.elnd"
    src = Path(filename).read_text()
    lexer = make_lexer(Lexer, src)
    try:
        for tok in lexer.scan():
            print(tok)
    except LexerError as exc:
        print(
            format_exception(exc, src, filename),
            file=sys.stderr
        )


if __name__ == '__main__':
    main()
