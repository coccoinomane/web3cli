from typing import List, TypedDict
from typing_extensions import NotRequired


class ChainFields(TypedDict):
    """Typing for chains.create and chains.update"""

    name: str
    chain_id: int
    coin: str
    tx_type: int
    middlewares: NotRequired[str]


class TxFields(TypedDict):
    """Typing for tx.create and tx.update"""

    hash: str
    chain: str
    to: str
    from_: str
    description: NotRequired[str]
    data: NotRequired[str]
    receipt: NotRequired[str]
    created_at: NotRequired[str]
    updated_at: NotRequired[str]
