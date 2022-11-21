def cut(s: str, n: int, suffix: str = "...") -> str:
    """Cut a string to n characters, replacing the excess
    characters with ellipsis"""
    if len(s) <= n:
        return s
    return s[0 : n - len(suffix)] + suffix
