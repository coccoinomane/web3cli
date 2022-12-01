from typing import List, TypedDict
from typing_extensions import NotRequired


class AddressFields(TypedDict):
    """Typing for Address model creation and update"""

    address: str
    name: str
    description: str


class ChainFields(TypedDict):
    """Typing for Chain model creation and update"""

    name: str
    chain_id: int
    coin: str
    tx_type: int
    middlewares: NotRequired[str]


class TxFields(TypedDict):
    """Typing for Tx model creation and update"""

    hash: str
    chain: str
    to: str
    from_: str
    description: NotRequired[str]
    data: NotRequired[str]
    receipt: NotRequired[str]
    created_at: NotRequired[str]
    updated_at: NotRequired[str]
