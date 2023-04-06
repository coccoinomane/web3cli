import pytest

import ape
from tests.ape.tests.helpers.uniswap import add_v2_liquidity, add_v2_liquidity_with_pair


@pytest.mark.xfail
@pytest.mark.local
@pytest.mark.contracts
def test_v2_add_liquidity_with_router(
    accounts: ape.managers.accounts.AccountManager,
    TST_0: ape.contracts.ContractInstance,
    TST_1: ape.contracts.ContractInstance,
    uniswap_v2_router: ape.contracts.ContractInstance,
    uniswap_v2_pair_TST_0_TST_1: ape.contracts.ContractInstance,
    # fn_isolation: Any,
) -> None:
    amount_0, amount_1 = 10**6, 10**6
    add_v2_liquidity(
        accounts[0],
        (TST_0, TST_1),
        (amount_0, amount_1),
        uniswap_v2_router,
    )
    # Test
    reserves = uniswap_v2_pair_TST_0_TST_1.getReserves()
    assert reserves[0] == amount_0
    assert reserves[1] == amount_1


@pytest.mark.xfail
@pytest.mark.local
@pytest.mark.contracts
def test_v2_add_liquidity_with_router_no_fixtures(
    accounts: ape.managers.accounts.AccountManager,
    # fn_isolation: Any,
    Token: ape.contracts.ContractContainer,
    UniswapV2Factory: ape.contracts.ContractContainer,
    UniswapV2Router02: ape.contracts.ContractContainer,
    UniswapV2Pair: ape.contracts.ContractContainer,
) -> None:
    # Deploy tokens
    tst0 = Token.deploy("TST_0", "TST_0", 18, 10**18, sender=accounts[0])
    tst1 = Token.deploy("TST_1", "TST_1", 18, 10**18, sender=accounts[0])
    weth = Token.deploy("WETH", "WETH", 18, 10**18, sender=accounts[0])
    # Deploy contracts
    factory = UniswapV2Factory.deploy(accounts[0], sender=accounts[0])
    router = UniswapV2Router02.deploy(factory, weth, sender=accounts[0])
    # Approve spender
    amount_0, amount_1 = 10**6, 10**6
    tst0.approve(router, amount_0, sender=accounts[0])
    tst1.approve(router, amount_1, sender=accounts[0])
    # Add liquidity with router (will create pair)
    router.addLiquidity(
        tst0,
        tst1,
        amount_0,
        amount_1,
        0,
        0,
        accounts[0],
        2**256 - 1,
        sender=accounts[0],
    )
    # Get pair contract
    pair_address = factory.getPair(tst0.address, tst1.address)
    pair = UniswapV2Pair.at(pair_address)
    # Test
    reserves = pair.getReserves()
    assert reserves[0] == amount_0
    assert reserves[1] == amount_1


@pytest.mark.local
@pytest.mark.contracts
def test_v2_add_liquidity_with_pair(
    accounts: ape.managers.accounts.AccountManager,
    TST_0: ape.contracts.ContractInstance,
    TST_1: ape.contracts.ContractInstance,
    uniswap_v2_factory: ape.contracts.ContractInstance,
    uniswap_v2_pair_TST_0_TST_1: ape.contracts.ContractInstance,
    UniswapV2Pair: ape.contracts.ContractContainer,
    # fn_isolation: Any,
) -> None:
    amount_0, amount_1 = 10**6, 10**6
    add_v2_liquidity_with_pair(
        accounts[0],
        (TST_0, TST_1),
        (amount_0, amount_1),
        uniswap_v2_factory,
        UniswapV2Pair,
    )
    # Test
    pair = UniswapV2Pair.at(uniswap_v2_factory.getPair(TST_0, TST_1))
    reserves = pair.getReserves()
    assert reserves[0] == amount_0
    assert reserves[1] == amount_1


@pytest.mark.local
@pytest.mark.contracts
def test_v2_add_liquidity_with_pair_no_fixtures(
    accounts: ape.managers.accounts.AccountManager,
    # fn_isolation: Any,
    Token: ape.contracts.ContractContainer,
    UniswapV2Factory: ape.contracts.ContractContainer,
    UniswapV2Pair: ape.contracts.ContractContainer,
) -> None:
    # Deply tokens
    tst0 = Token.deploy("TST_0", "TST_0", 18, 10**21, sender=accounts[0])
    tst1 = Token.deploy("TST_1", "TST_1", 18, 10**21, sender=accounts[0])
    factory = UniswapV2Factory.deploy(accounts[0], sender=accounts[0])
    # Create pair
    factory.createPair(tst0, tst1, sender=accounts[0])
    pair_address = factory.getPair(tst0, tst1)
    pair = UniswapV2Pair.at(pair_address)
    # Add liquidity with mint
    amount_0, amount_1 = 10**6, 10**6
    tst0.transfer(pair.address, amount_0, sender=accounts[0])
    tst1.transfer(pair.address, amount_1, sender=accounts[0])
    pair.mint(accounts[0].address, sender=accounts[0])
    # Test
    reserves = pair.getReserves()
    assert reserves[0] == amount_0
    assert reserves[1] == amount_1
