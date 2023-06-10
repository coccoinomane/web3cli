from typing import List, Type

import web3
from web3 import Web3

from web3core.exceptions import AddressNotResolved
from web3core.models.address import Address
from web3core.models.base_model import BaseModel
from web3core.models.contract import Contract
from web3core.models.signer import Signer


def resolve_address(
    address_or_name: str,
    models: List[Type[BaseModel]] = [Address, Signer, Contract],
    chain: str = None,
    to_checksum: bool = True,
) -> str:
    """Search the given models for records with the given name,
    and if the record is found, return the corresponding address.

    If an actual valid address is passed (0x...) then return it.

    For chain-aware models, like Contract, the chain must be
    specified, too, otherwise the first matching record is returned.
    """

    def format(address: str) -> str:
        if to_checksum:
            return Web3.to_checksum_address(address)
        return address

    if is_valid_address(address_or_name):
        return format(address_or_name)

    for model in models:
        try:
            if hasattr(model, "chain"):
                if chain is not None:
                    return format(model.get(name=address_or_name, chain=chain).address)
                raise ValueError(
                    f"Chain argument must be specified for {model.__name__} model, but was not"
                )
            else:
                return format(model.get(name=address_or_name).address)
        except model.DoesNotExist:
            pass

    raise AddressNotResolved(
        f"Could not resolve '{address_or_name}': neither a valid address nor a name of a stored address"
    )


def is_valid_address(address: str) -> bool:
    """Is the address a valid EVM address?"""
    return web3.main.is_address(address)
