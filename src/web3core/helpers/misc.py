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


def to_bool(s: str) -> bool:
    """Cast a string to False or True. The string case is ignored.

    >>> to_bool("true") == True
    >>> to_bool("false") == False
    >>> to_bool("0") == False
    >>> to_bool("1") == True
    >>> to_bool("foo") == ValueError
    """
    if s.lower() in ("false", "0"):
        return False
    elif s.lower() in ("true", "1"):
        return True
    else:
        raise ValueError(f"Cannot cast {s} to bool")
