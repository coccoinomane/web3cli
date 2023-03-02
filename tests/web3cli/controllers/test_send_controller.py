import pytest

from brownie.network.account import Account as BrownieAccount
from brownie.network.contract import Contract as BrownieContract
from tests.seed import seed_local_token
from tests.web3cli.main import Web3CliTest


@pytest.mark.local
def test_send_eth(app: Web3CliTest, alice: BrownieAccount, bob: BrownieAccount) -> None:
    bob_balance = bob.balance()
    app.set_args(
        ["--signer", "alice", "send", bob.address, "1", "ETH", "--force"]
    ).run()
    assert bob.balance() == bob_balance + 10**18


@pytest.mark.local
def test_send_eth_using_address_tag(
    app: Web3CliTest, alice: BrownieAccount, bob: BrownieAccount
) -> None:
    bob_balance = bob.balance()
    app.set_args(["--signer", "alice", "send", "bob", "1", "ETH", "--force"]).run()
    assert bob.balance() == bob_balance + 10**18


@pytest.mark.local
def test_send_eth_wei(
    app: Web3CliTest, alice: BrownieAccount, bob: BrownieAccount
) -> None:
    bob_balance = bob.balance()
    app.set_args(
        ["--signer", "alice", "send", bob.address, "1", "ETH", "wei", "--force"]
    ).run()
    assert bob.balance() == bob_balance + 1


@pytest.mark.local
def test_send_token(
    app: Web3CliTest,
    alice: BrownieAccount,
    bob: BrownieAccount,
    TST: BrownieContract,
) -> None:
    bob_balance = TST.balanceOf(bob.address)
    seed_local_token(app, TST)
    app.set_args(
        ["--signer", "alice", "send", bob.address, "1", TST.symbol(), "--force"]
    ).run()
    assert TST.balanceOf(bob.address) == bob_balance + 10**18


@pytest.mark.local
def test_send_token_with_alias(
    app: Web3CliTest,
    alice: BrownieAccount,
    bob: BrownieAccount,
    TST: BrownieContract,
) -> None:
    bob_balance = TST.balanceOf(bob.address)
    seed_local_token(app, TST)
    app.set_args(
        ["--signer", "alice", "send", "bob", "1", TST.symbol(), "--force"]
    ).run()
    assert TST.balanceOf(bob.address) == bob_balance + 10**18


@pytest.mark.local
def test_send_token_smallest(
    app: Web3CliTest,
    alice: BrownieAccount,
    bob: BrownieAccount,
    TST: BrownieContract,
) -> None:
    bob_balance = TST.balanceOf(bob.address)
    seed_local_token(app, TST)
    app.set_args(
        [
            "--signer",
            "alice",
            "send",
            bob.address,
            "1",
            TST.symbol(),
            "smallest",
            "--force",
        ]
    ).run()
    assert TST.balanceOf(bob.address) == bob_balance + 1


@pytest.mark.local
def test_send_token6(
    app: Web3CliTest,
    alice: BrownieAccount,
    bob: BrownieAccount,
    TST6: BrownieContract,
) -> None:
    bob_balance = TST6.balanceOf(bob.address)
    seed_local_token(app, TST6)
    app.set_args(
        ["--signer", "alice", "send", bob.address, "1", TST6.symbol(), "--force"]
    ).run()
    assert TST6.balanceOf(bob.address) == bob_balance + 10**6


@pytest.mark.local
def test_send_token6_smallest(
    app: Web3CliTest,
    alice: BrownieAccount,
    bob: BrownieAccount,
    TST6: BrownieContract,
) -> None:
    bob_balance = TST6.balanceOf(bob.address)
    seed_local_token(app, TST6)
    app.set_args(
        [
            "--signer",
            "alice",
            "send",
            bob.address,
            "1",
            TST6.symbol(),
            "smallest",
            "--force",
        ]
    ).run()
    assert TST6.balanceOf(bob.address) == bob_balance + 1
