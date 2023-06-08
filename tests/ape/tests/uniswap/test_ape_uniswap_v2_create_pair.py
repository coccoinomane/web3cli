import pytest

import ape


@pytest.mark.local
@pytest.mark.contracts
def test_v2_create_pair(
    uniswap_v2_pair_WETH_TST: ape.contracts.ContractInstance,
    WETH: ape.contracts.ContractInstance,
    TST: ape.contracts.ContractInstance,
    uniswap_v2_factory: ape.contracts.ContractInstance,
) -> None:
    reserves = uniswap_v2_pair_WETH_TST.getReserves()
    assert reserves[0] == 0
    assert reserves[1] == 0
    assert uniswap_v2_pair_WETH_TST.factory() == uniswap_v2_factory.address
    # Tokens are interchangeable
    assert (
        uniswap_v2_pair_WETH_TST.token0() == TST.address
        and uniswap_v2_pair_WETH_TST.token1() == WETH.address
    ) or (
        uniswap_v2_pair_WETH_TST.token0() == WETH.address
        and uniswap_v2_pair_WETH_TST.token1() == TST.address
    )
