from typing import List, Type

from peewee import Model

from web3core.models.address import Address
from web3core.models.chain import Chain, ChainRpc, Rpc
from web3core.models.contract import Contract, ContractType
from web3core.models.signer import Signer
from web3core.models.tx import Tx

MODELS: List[Type[Model]] = [
    Signer,
    Address,
    Chain,
    Rpc,
    ChainRpc,
    Tx,
    ContractType,
    Contract,
]
