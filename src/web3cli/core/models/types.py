from typing import List, TypedDict
from typing_extensions import NotRequired


class RpcFields(TypedDict):
    """Typing for Rpc model creation and update"""

    url: str


class ChainFields(TypedDict):
    """Typing for Chain model creation and update"""

    name: str
    chain_id: int
    coin: str
    tx_type: int
    middlewares: str
    rpcs: NotRequired[List[RpcFields]]


class AddressFields(TypedDict):
    """Typing for Address model creation and update"""

    address: str
    name: str
    description: str


class SignerFields(TypedDict):
    """Typing for Signer model creation and update"""

    name: str
    address: str
    key: bytes


class TxFields(TypedDict):
    """Typing for Tx model creation and update"""

    hash: str
    chain: str
    to: str
    from_: str
    value: NotRequired[str]
    gas: NotRequired[int]
    gas_price: NotRequired[str]
    description: NotRequired[str]
    data: NotRequired[str]
    receipt: NotRequired[str]
    created_at: NotRequired[str]
    updated_at: NotRequired[str]
