from typing import Any
import sys


def yes_or_exit(
    question: str = "Type 'yes' or 'y' to proceed: ",
    exit_message: str = "Exiting...",
    logger: Any = print,
    exit_code: int = 0,
) -> bool:
    """Ask a question and exit the sript if the answer is not in (yes, y, YES or Y)"""
    answer = input(question)
    yes = answer.lower() in ("yes", "y")
    if not yes:
        if exit_message:
            logger(exit_message)
        sys.exit(exit_code)
