from typing import List

from web3 import Web3
from web3._utils.abi import abi_to_signature, filter_by_name
from web3.types import ABI


def abi_to_function_names(abi: ABI) -> List[str]:
    """Given an ABI, return the names of its function"""
    contract = Web3().eth.contract(abi=abi)
    return [f for f in contract.functions]


def abi_to_function_signatures(abi: ABI) -> List[str]:
    """Given an ABI, return the signatures of its function"""
    names = abi_to_function_names(abi)
    abis = [filter_by_name(name, abi)[0] for name in names]
    return [abi_to_signature(abi) for abi in abis]
