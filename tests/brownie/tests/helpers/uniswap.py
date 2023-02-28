"""Helper functions to better run tests"""


from typing import Any, Tuple

from brownie.network.account import Account as BrownieAccount
from brownie.network.contract import Contract as BrownieContract
from brownie.network.contract import ContractContainer as BrownieContractContainer


def deploy_v2_pair(
    UniswapV2Pair: BrownieContractContainer,
    account: BrownieAccount,
    uniswap_v2_factory: BrownieContract,
    tokens: Tuple[BrownieContract, BrownieContract],
) -> BrownieContract:
    """Deply a liquidity pair for the given tokens. The pair will be deployed
    by the given account and returned as a contract object."""
    uniswap_v2_factory.createPair(
        tokens[0].address, tokens[1].address, {"from": account}
    )
    address = uniswap_v2_factory.getPair(tokens[0].address, tokens[1].address)
    return UniswapV2Pair.at(address)


def add_v2_liquidity(
    account: BrownieAccount,
    tokens: Tuple[BrownieContract, BrownieContract],
    liquidity: Tuple[int, int],
    uniswap_v2_router: BrownieContract,
) -> Any:
    """Add liquidity to the given pair of tokens, using the router. Express
    token amounts in token units.

    Please note that the router's contract allows you to add liquidity also
    if the pair does not exist yet. In this case, the pair will be created
    and the liquidity added in the same transaction.

    ARGUMENTS
    _________

    account: The account to deploy the pair from.
    tokens: A tuple of the two tokens to add liquidity for.
    liquidity: An optional tuple of the amount of liquidity to add to the pair.
        The amounts should be expressed in token units.
    UniswapV2Router: The UniswapV2Router contract.

    RETURNS
    _______


    """
    amount0 = liquidity[0] * 10 ** tokens[0].decimals()
    amount1 = liquidity[1] * 10 ** tokens[1].decimals()
    tokens[0].approve(uniswap_v2_router, amount0, {"from": account})
    tokens[1].approve(uniswap_v2_router, amount1, {"from": account})
    # Print all arguments
    print(
        f"addLiquidity('{tokens[0].address}', '{tokens[1].address}', {amount0}, {amount1}, 0, 0, '{account}', 2**256 - 1, {{'from': '{account}'}})"
    )
    return uniswap_v2_router.addLiquidity(
        tokens[0],
        tokens[1],
        amount0,
        amount1,
        0,
        0,
        account,
        2**256 - 1,
        {"from": account},
    )
