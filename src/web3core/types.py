from typing import Any, Callable, Literal, TypedDict

from eth_account.datastructures import SignedTransaction
from web3.types import TxData, TxParams, TxReceipt

Logger = Callable[[str], None]


class TxLife(TypedDict):
    """A dictionary containing the life cylce of a transaction.

    Functions that return a TxSummary should return a dict with the following
    keys:
        - params: The transaction parameters as they were sent to the
            blockchain.
        - hash: The transaction hash.
        - sig: The signed transaction dict with properties:
            - rawTransaction: The raw transaction.
            - hash: The transaction hash.
            - r: The r value of the signature.
            - s: The s value of the signature.
            - v: The v value of the signature.
        - output: The output of the function call. This is present
            only if the tx called a contract function with eth_call.
        - data: The transaction data as returned by eth_getTransactionByHash.
            This is only present if the transaction was sent.
        - receipt: The transaction receipt. This is only present if the
            transaction was sent.
    """

    params: TxParams
    hash: str
    sig: SignedTransaction
    output: Any
    data: TxData
    receipt: TxReceipt


TX_LIFE_PROPERTIES = list(TxLife.__annotations__.keys())

TxLifeProperty = Literal["params", "hash", "sig", "output", "data", "receipt"]
