from web3.contract.contract import Contract as Web3Contract

from web3core.helpers.client_factory import make_contract_client
from web3core.models.chain import Chain


def get_web3_contract(contract_name: str, chain: Chain) -> Web3Contract:
    """Given a contract name and a chain, return the corresponding
    web3py contract object"""
    return make_contract_client(contract_name, chain).contract
