from typing import Any
import sys
from web3cli.core.types import Logger


def yes_or_exit(
    question: str = "Type 'yes' or 'y' to proceed: ",
    exit_message: str = "Exiting...",
    logger: Logger = print,
    exit_code: int = 0,
) -> str:
    """Ask a question and exit the script if the answer is not in
    (yes, y, YES or Y). Return the answer."""
    answer = input(question)
    yes = answer.lower() in ("yes", "y")
    if not yes:
        if exit_message:
            logger(exit_message)
        sys.exit(exit_code)
    return answer
