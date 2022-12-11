from typing import Any
import sys
from web3cli.core.types import Logger


def yes_or_exit(
    prompt: str = "Type 'yes' or 'y' to proceed: ",
    exit_msg: str = "Exiting...",
    intro: str = None,
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
