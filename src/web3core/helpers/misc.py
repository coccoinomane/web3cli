import decimal
import sys
from typing import Union

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
        dec = decimal.Decimal(string_value)
        if dec.as_integer_ratio()[1] != 1:
            raise ValueError(f"String {string_value} is not an integer")
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
