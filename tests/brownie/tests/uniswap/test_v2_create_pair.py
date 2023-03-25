import pytest

from brownie.network.contract import Contract as BrownieContract


@pytest.mark.local
@pytest.mark.contracts
def test_v2_pair(
    uniswap_v2_pair_WETH_TST: BrownieContract,
    WETH: BrownieContract,
    TST: BrownieContract,
    uniswap_v2_factory: BrownieContract,
) -> None:
    reserves = uniswap_v2_pair_WETH_TST.getReserves()
    assert reserves[0] == 0
    assert reserves[1] == 0
    assert uniswap_v2_pair_WETH_TST.factory() == uniswap_v2_factory.address
    assert uniswap_v2_pair_WETH_TST.token0() == WETH.address
    assert uniswap_v2_pair_WETH_TST.token1() == TST.address
