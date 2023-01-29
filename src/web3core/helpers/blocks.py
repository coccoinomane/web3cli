from typing import Union

from web3._utils.blocks import select_method_for_block_identifier

BLOCK_PREDEFINED_IDENTIFIERS = {"latest", "pending", "earliest", "safe", "finalized"}


def get_block_type(block_identifier: Union[str, int]) -> str:
    """Return the type of the given block identifier.

    The returned value is one of these:
     - "number": the block identifier is an integer or a string representing an
       integer (e.g. "123" or "0xabc")
     - "hash": the block identifier is a string representing a SHA256 hash
     - "predefined": the block identifier is one of the predefined block
       identifiers ("latest", "pending", "earliest", "safe", "finalized")

    Raises ValueError if the given block identifier is not valid.
    """
    return select_method_for_block_identifier(
        block_identifier, if_hash="hash", if_number="number", if_predefined="predefined"
    )
