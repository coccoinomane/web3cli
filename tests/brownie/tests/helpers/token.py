"""Helper functions to better run tests"""


from typing import List

from brownie.network.account import Account as BrownieAccount
from brownie.network.contract import Contract as BrownieContract
from brownie.network.contract import ContractContainer as BrownieContractContainer


def deploy_token(
    Token: BrownieContractContainer,
    accounts: List[BrownieAccount],
    name: str = "Test Token",
    symbol: str = "TST",
    decimals: int = 18,
    initial_supply: int = 10000,
    distribute: bool = True,
) -> BrownieContract:
    """Deploy a test token, and distribute it to all accounts. The token
    will be deployed by alice (accounts[0]) and optionally distributed
    to all other accounts."""
    token = Token.deploy(
        name, symbol, decimals, initial_supply * 10**decimals, {"from": accounts[0]}
    )
    if distribute:
        for account in accounts[1:]:
            token.transfer(account, 1000 * 10**decimals, {"from": accounts[0]})
    return token
