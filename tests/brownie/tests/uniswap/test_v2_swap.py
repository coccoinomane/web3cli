from typing import Any, List

import pytest

from brownie.network.account import Account as BrownieAccount
from brownie.network.contract import Contract as BrownieContract


@pytest.mark.local
def test_v2_swap_exact_tokens_for_tokens(
    accounts: List[BrownieAccount],
    TST_0: BrownieContract,
    TST_1: BrownieContract,
    uniswap_v2_router: BrownieContract,
    uniswap_v2_pair_TST_0_TST_1_with_liquidity: BrownieContract,
    fn_isolation: Any,
) -> None:
    # Compute amounts and balances
    amount_in = 10**6
    balance_0 = TST_0.balanceOf(accounts[0])
    balance_1 = TST_1.balanceOf(accounts[0])
    reserves = uniswap_v2_pair_TST_0_TST_1_with_liquidity.getReserves()
    # Approve spender
    TST_0.approve(uniswap_v2_router, amount_in, {"from": accounts[0]})
    # Swap
    uniswap_v2_router.swapExactTokensForTokens(
        amount_in, 0, [TST_0, TST_1], accounts[0], 2**256 - 1, {"from": accounts[0]}
    )
    # Test
    balance_0_after = TST_0.balanceOf(accounts[0])
    balance_1_after = TST_1.balanceOf(accounts[0])
    reserves_after = uniswap_v2_pair_TST_0_TST_1_with_liquidity.getReserves()
    assert reserves_after[0] == reserves[0] + amount_in
    assert balance_0_after > balance_0 - amount_in
    assert balance_1_after > balance_1
