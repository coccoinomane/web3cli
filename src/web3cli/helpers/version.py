from typing import Tuple
from cement.utils.version import get_version_banner
from cement.utils.version import get_version as cement_get_version

VERSION = (0, 9, 2, "alpha", 0)


def get_version_number(version: Tuple[int, int, int, str, int] = VERSION) -> str:
    return cement_get_version(version)


def get_version_message() -> str:
    return "web3cli %s\n%s" % (
        get_version_number(),
        get_version_banner(),
    )
