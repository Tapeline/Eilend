from hypothesis import strategies, assume

from eilend.lexer.token import (
    ALLOWED_NAME_CHARS,
    ALLOWED_NAME_START_CHARS,
    KEYWORDS,
)


@strategies.composite
def valid_number_literal(draw):
    return draw(strategies.from_regex(
        r"[0-9]+(\.[0-9]+)?",
        fullmatch=True
    ))


@strategies.composite
def valid_string_literal(draw):
    text = draw(strategies.text(
        alphabet=strategies.characters(
            codec="utf-8", exclude_characters="\n\r\f\"\\"
        )
    ))
    escape = ""
    if draw(strategies.booleans()):
        escape = draw(strategies.from_regex(
            r'\\[abfnrtv\\"]', fullmatch=True
        ))
    return f'"{text}{escape}"'


@strategies.composite
def valid_identifier(draw):
    start = draw(
        strategies.text(alphabet=ALLOWED_NAME_START_CHARS, min_size=1)
    )
    other = draw(
        strategies.text(alphabet=ALLOWED_NAME_CHARS)
    )
    identifier = start + other
    assume(identifier not in KEYWORDS)
    return identifier


@strategies.composite
def valid_comment(draw):
    text = draw(
        strategies.text(
            alphabet=strategies.characters(
                codec="utf-8", exclude_characters="\n\r\f"
            )
        )
    )
    return f"#{text}"
