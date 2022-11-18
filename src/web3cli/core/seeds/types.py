from typing import List, TypedDict
from typing_extensions import NotRequired


class ChainSeed(TypedDict):
    """
    Dictionary representing a chain and its rpcs
    """

    name: str
    chain_id: int
    coin: str
    tx_type: int
    middlewares: List[str]
    rpcs: List[str]
