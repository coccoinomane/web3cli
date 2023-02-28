from brownie.network.contract import Contract as BrownieContract


def test_v2_pair(
    uniswap_v2_pair_weth_tst: BrownieContract,
    weth: BrownieContract,
    token: BrownieContract,
    uniswap_v2_factory: BrownieContract,
) -> None:
    reserves = uniswap_v2_pair_weth_tst.getReserves()
    assert reserves[0] == 0
    assert reserves[1] == 0
    assert uniswap_v2_pair_weth_tst.factory() == uniswap_v2_factory.address
    assert uniswap_v2_pair_weth_tst.token0() == weth.address
    assert uniswap_v2_pair_weth_tst.token1() == token.address
