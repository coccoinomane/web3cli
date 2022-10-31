from typing import Tuple
from cement.utils.version import get_version as cement_get_version

VERSION = (0, 1, 5, "alpha", 0)


def get_version(version: Tuple[int, int, int, str, int] = VERSION) -> str:
    return cement_get_version(version)
