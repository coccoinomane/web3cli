"""Utility functions for web3.py"""

import pprint
from typing import Any, Union

from web3.datastructures import AttributeDict
from web3.types import TxReceipt


def format_attribute_dict(
    attributeDict: Union[TxReceipt, AttributeDict[str, Any]],
    indent: int = 4,
    nestLevel: int = 0,
) -> str:
    """
    Web3 often returns AttributeDict instead of simple Dictionaries;
    this function return a pretty string with the AttributeDict content
    """
    prefix = nestLevel * indent * " "
    output = prefix + "{\n"
    for key, value in attributeDict.items():
        if isinstance(value, AttributeDict):
            output += prefix + format_attribute_dict(value, indent, nestLevel + 1)
            output += "\n"
        else:
            output += prefix + " " * indent
            output += f"{key} -> {pprint.pformat(value, indent=indent)}"
            output += "\n"
    output += prefix + "}"

    return output
