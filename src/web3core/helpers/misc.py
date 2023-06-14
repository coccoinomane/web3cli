import codecs
import decimal
import re
import sys
from typing import Any, Dict, Union

from web3core.types import Logger


def yes_or_exit(
    prompt: str = "Type 'yes' or 'y' to proceed: ",
    exit_msg: str = "Exiting...",
    intro: str = "",
    logger: Logger = print,
    exit_code: int = 0,
) -> str:
    """Ask a question and exit the script if the answer is not in
    (yes, y, YES or Y). Return the answer."""
    answer = input(intro + prompt)
    yes = answer.lower() in ("yes", "y")
    if not yes:
        if exit_msg:
            logger(exit_msg)
        sys.exit(exit_code)
    return answer


def to_number(s: str) -> Union[int, float]:
    """Cast a string to either an integer or a float"""
    try:
        return int(s)
    except ValueError:
        return float(s)


def to_int(string_value: str, allow_exp_notation: bool = True) -> int:
    """Convert a string to an integer.

    Args:
        string_value: The string to convert.
        allow_exp_notation: Whether to allow exponential notation for integers
        (e.g. 5e18 will be translated to 5000000000000000000). This is done in
        a way that prevents floating point errors.
    """
    if allow_exp_notation:
        try:
            dec = decimal.Decimal(string_value)
        except decimal.InvalidOperation:
            raise ValueError(f"String '{string_value}' cannot be converted to a number")
        if dec.as_integer_ratio()[1] != 1:
            raise ValueError(
                f"String '{string_value}' cannot be converted to an integer"
            )
        return int(dec)
    return int(string_value)


def to_bool(s: str) -> bool:
    """Cast a string to False or True.

    Cast a string to False or True, ignoring both case and
    leading/trailing whitespace. Raise ValueError if the string
    is not a valid boolean value.

    EXAMPLES:
    >>> to_bool("true") == True
    >>> to_bool("false") == False
    >>> to_bool(" true ") == True
    >>> to_bool(" false ") == False
    >>> to_bool("0") == False
    >>> to_bool("1") == True
    >>> to_bool("foo") == ValueError
    """
    clean_string = s.lower().strip()
    if clean_string in ("false", "0"):
        return False
    elif clean_string in ("true", "1"):
        return True
    else:
        raise ValueError(f"Cannot cast {s} to bool")


def are_mutually_exclusive(*args: bool) -> bool:
    """Check that maximum one of the arguments is True."""
    return sum(args) <= 1


def decode_escapes(s: str) -> str:
    """Decode escape sequences in a string, for example
    \\n > \n, \\u00e9 > é, etc.

    Source: https://stackoverflow.com/a/24519338/2972183"""

    def decode_match(match: Any) -> str:
        return codecs.decode(match.group(0), "unicode-escape")

    ESCAPE_SEQUENCE_RE = re.compile(
        r"""
        ( \\U........      # 8-digit hex escapes
        | \\u....          # 4-digit hex escapes
        | \\x..            # 2-digit hex escapes
        | \\[0-7]{1,3}     # Octal escapes
        | \\N\{[^}]+\}     # Unicode characters by name
        | \\[\\'"abfnrtv]  # Single-character escapes
        )""",
        re.UNICODE | re.VERBOSE,
    )

    return ESCAPE_SEQUENCE_RE.sub(decode_match, s)


def replace_all(text: str, dic: Dict[str, Any]) -> str:
    """Replace substrings in a string, based on a dictionary.

    Source: https://stackoverflow.com/a/6117042/2972183"""
    for i, j in dic.items():
        text = text.replace(i, str(j))
    return text
