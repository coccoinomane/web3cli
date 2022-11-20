from typing import List, TypedDict
from typing_extensions import NotRequired


class ChainFields(TypedDict):
    """A dict that maps to a row in the chains table"""

    name: str
    chain_id: int
    coin: str
    tx_type: int
    middlewares: NotRequired[str]
