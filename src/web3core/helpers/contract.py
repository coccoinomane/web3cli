from typing import Union

from web3.contract.contract import Contract as Web3Contract

from web3core.helpers.client_factory import make_contract_client
from web3core.models.chain import Chain
from web3core.models.contract import Contract


def get_web3_contract(contract: Union[Contract, str], chain: Chain) -> Web3Contract:
    """Given a contract name and a chain, return the corresponding
    web3py contract object"""
    return make_contract_client(contract, chain).contract
