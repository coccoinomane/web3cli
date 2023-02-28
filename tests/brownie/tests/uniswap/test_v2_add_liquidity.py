from typing import List

import pytest

from brownie.network.account import Account as BrownieAccount
from brownie.network.contract import Contract as BrownieContract
from tests.brownie.tests.helpers.uniswap import add_v2_liquidity


@pytest.mark.xfail
def test_v2_liquidity(
    uniswap_v2_pair_weth_tst: BrownieContract,
    weth: BrownieContract,
    token: BrownieContract,
    accounts: List[BrownieAccount],
    uniswap_v2_router: BrownieContract,
) -> None:
    add_v2_liquidity(
        accounts[0],
        (weth, token),
        (100, 100),
        uniswap_v2_router,
    )
    reserves = uniswap_v2_pair_weth_tst.getReserves()
    assert reserves[0] == 100
    assert reserves[1] == 100
