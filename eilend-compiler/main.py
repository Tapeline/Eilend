import sys
from pathlib import Path
from pprint import pprint

from syntactix.lexical.exceptions import LexerError
from syntactix.parser.exceptions import ParserError
from syntactix.error_formatter import format_exception

from eilend.parser.parser import parse_tokens
from tests.lexer.conftest import call_lexer


def main() -> None:
    src = Path("test.elnd").read_text()
    try:
        tokens = call_lexer(src)
        nodes = parse_tokens(tokens)
        pprint(nodes)
    except (LexerError, ParserError) as exc:
        print(format_exception(exc, src, "test.elnd"), file=sys.stderr)


if __name__ == '__main__':
    main()
