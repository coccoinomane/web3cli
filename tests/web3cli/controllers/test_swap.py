import pytest

from brownie.network.account import Account as BrownieAccount
from brownie.network.contract import Contract as BrownieContract
from tests.seed import seed_local_contract, seed_local_token
from tests.web3cli.main import Web3CliTest


@pytest.mark.local
def test_swap(
    app: Web3CliTest,
    TST_0: BrownieContract,
    TST_1: BrownieContract,
    alice: BrownieAccount,
    uniswap_v2_router: BrownieContract,
    uniswap_v2_pair_TST_0_TST_1_with_liquidity: BrownieContract,
) -> None:
    # Save Alice's balances of TST_0 and TST_1
    balance_0 = TST_0.balanceOf(alice.address)
    TST_1.balanceOf(alice.address)
    # Get the current reserves of the trading pair
    reserves = uniswap_v2_pair_TST_0_TST_1_with_liquidity.getReserves()
    reserves[0] * reserves[1]
    # Create the token contracts
    seed_local_token(app, TST_0)
    seed_local_token(app, TST_1)
    seed_local_contract(app, "uniswap_v2", uniswap_v2_router, "uniswap_v2")
    # Alice swaps 0.1 TST_0 for TST_1
    app.set_args(
        [
            "--signer",
            "alice",
            "swap",
            "uniswap_v2",
            "0.1",
            "tst_0",
            "tst_1",
        ]
    ).run()
    # Alice should have spent 0.1 TST_0
    assert TST_0.balanceOf(alice.address) == balance_0 - 10**17
    # Alice should have received the equivalent amount of TST_1
    # respecting the constant product law:
    # TST_1 = k / (TST_0 + 10**17)
    # balance_1_expected = k / (reserves[0] + 10**17)
    # assert TST_1.balanceOf(alice.address) == balance_1 + balance_1_expected
