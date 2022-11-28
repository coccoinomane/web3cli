from textwrap import wrap as lib_wrap
from typing import List


def cut(s: str, n: int, suffix: str = "...") -> str:
    """Cut a string to n characters, replacing the excess
    characters with ellipsis"""
    if len(s) <= n or n <= len(suffix):
        return s
    return s[0 : n - len(suffix)] + suffix


def wrap(s: str, n: int) -> List[str]:
    """Given a string split it in substrings of length n"""
    return lib_wrap(s, n)
