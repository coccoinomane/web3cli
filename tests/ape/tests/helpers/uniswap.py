"""Helper functions to better run tests"""


from typing import Any, Tuple

import ape


def deploy_v2_pair(
    account: ape.api.AccountAPI,
    tokens: Tuple[ape.contracts.ContractInstance, ape.contracts.ContractInstance],
    uniswap_v2_factory: ape.contracts.ContractInstance,
    UniswapV2Pair: ape.contracts.ContractContainer,
) -> ape.contracts.ContractInstance:
    """Deply a liquidity pair for the given tokens. The pair will be deployed
    by the given account and returned as a contract object."""
    uniswap_v2_factory.createPair(tokens[0].address, tokens[1].address, sender=account)
    address = uniswap_v2_factory.getPair(tokens[0].address, tokens[1].address)
    return UniswapV2Pair.at(address)


def add_v2_liquidity(
    account: ape.api.AccountAPI,
    tokens: Tuple[ape.contracts.ContractInstance, ape.contracts.ContractInstance],
    liquidity: Tuple[int, int],
    router: ape.contracts.ContractInstance,
) -> Any:
    """Add liquidity to the given pair of tokens, using the router.

    TODO: Does not work, reverts on 'address public feeTo'in UniswapV2Factory.sol

    Please note that the router's contract allows you to add liquidity also
    if the pair does not exist yet. In this case, the pair will be created
    and the liquidity added in the same transaction.

    ARGUMENTS
    _________
    account: The account to deploy the pair from.
    tokens: A tuple of the two tokens to add liquidity for.
    liquidity: A tuple of the amount of liquidity to add to the pair.
        The amounts should be expressed in token units.
    router: The UniswapV2Router ape contract.

    RETURNS
    _______
    The transaction receipt.
    """
    # Approve the router to spend the tokens
    raise_if_liquidity_too_small(liquidity[0], liquidity[1])
    tokens[0].approve(router, liquidity[0], sender=account)
    tokens[1].approve(router, liquidity[1], sender=account)
    # Add liquidity
    return router.addLiquidity(
        tokens[0],
        tokens[1],
        liquidity[0],
        liquidity[1],
        0,
        0,
        account,
        2**256 - 1,
        sender=account,
    )


def add_v2_liquidity_with_pair(
    account: ape.api.AccountAPI,
    tokens: Tuple[ape.contracts.ContractInstance, ape.contracts.ContractInstance],
    liquidity: Tuple[int, int],
    factory: ape.contracts.ContractInstance,
    UniswapV2Pair: ape.contracts.ContractContainer,
) -> Any:
    """Add liquidity to the given pair of tokens, using the pair's contract.

    Raises an exception if the pair does not exist yet.

    ARGUMENTS
    _________
    account: The account to deploy the pair from.
    tokens: A tuple of the two tokens to add liquidity for.
    liquidity: A tuple of the amount of liquidity to add to the pair.
        The amounts should be expressed in token units.
    factory: The UniswapV2Factory contract, needed to find the pair.

    RETURNS
    _______
    The transaction receipt.
    """
    # Get pair
    pair_address = factory.getPair(tokens[0], tokens[1])
    if pair_address == ape.utils.ZERO_ADDRESS:
        raise ValueError("Pair does not exist yet")
    pair = UniswapV2Pair.at(pair_address)
    # Transfer the tokens to the pair
    raise_if_liquidity_too_small(liquidity[0], liquidity[1])
    tokens[0].transfer(pair, liquidity[0], sender=account)
    tokens[1].transfer(pair, liquidity[1], sender=account)
    # Add liquidity
    return pair.mint(account, sender=account)


def raise_if_liquidity_too_small(amount_0: int, amount_1: int) -> None:
    """Raise an exception if the liquidity provided for the pair (in Wei)
    is too small"""
    if amount_0 < 10**4 or amount_1 < 10**4:
        raise ValueError(
            "Liquidity too small. Please add more liquidity to the pair lest the transaction may revert."
        )
