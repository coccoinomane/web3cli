from typing import Union
from urllib.parse import urlparse

from web3core.helpers.blocks import get_block_type


def is_valid_block_identifier(block_identifier: Union[str, int]) -> bool:
    """Return True if the given block identifier is valid, False otherwise"""
    try:
        get_block_type(block_identifier)
        return True
    except ValueError:
        return False


def is_valid_url(url: str) -> bool:
    """Return false if the given string is not a valid URL"""
    result = urlparse(url)
    return all([result.scheme, result.netloc])
