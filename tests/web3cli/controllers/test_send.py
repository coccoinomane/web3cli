import pytest

from brownie.network import Chain as BrownieChain
from brownie.network.account import Account
from brownie.network.contract import Contract as BrownieContract
from tests.seed import seed_local_token
from tests.web3cli.main import Web3CliTest


@pytest.mark.local
def test_send_eth(
    app: Web3CliTest, alice: Account, bob: Account, chain: BrownieChain
) -> None:
    chain.reset()
    bob_balance = bob.balance()
    app.set_args(
        ["--signer", "alice", "send", bob.address, "1", "ETH", "--force"]
    ).run()
    assert bob.balance() == bob_balance + 10**18


@pytest.mark.local
def test_send_eth_using_address_tag(
    app: Web3CliTest, alice: Account, bob: Account, chain: BrownieChain
) -> None:
    chain.reset()
    bob_balance = bob.balance()
    app.set_args(["--signer", "alice", "send", "bob", "1", "ETH", "--force"]).run()
    assert bob.balance() == bob_balance + 10**18


@pytest.mark.local
def test_send_eth_wei(
    app: Web3CliTest, alice: Account, bob: Account, chain: BrownieChain
) -> None:
    chain.reset()
    bob_balance = bob.balance()
    app.set_args(
        ["--signer", "alice", "send", bob.address, "1", "ETH", "wei", "--force"]
    ).run()
    assert bob.balance() == bob_balance + 1


@pytest.mark.local
def test_send_token18(
    app: Web3CliTest,
    alice: Account,
    bob: Account,
    token18: BrownieContract,
) -> None:
    bob_balance = token18.balanceOf(bob.address)
    seed_local_token(app, token18)
    app.set_args(
        ["--signer", "alice", "send", bob.address, "1", token18.symbol(), "--force"]
    ).run()
    assert token18.balanceOf(bob.address) == bob_balance + 10**18


@pytest.mark.local
def test_send_token18_smallest(
    app: Web3CliTest,
    alice: Account,
    bob: Account,
    token18: BrownieContract,
) -> None:
    bob_balance = token18.balanceOf(bob.address)
    seed_local_token(app, token18)
    app.set_args(
        [
            "--signer",
            "alice",
            "send",
            bob.address,
            "1",
            token18.symbol(),
            "smallest",
            "--force",
        ]
    ).run()
    assert token18.balanceOf(bob.address) == bob_balance + 1


@pytest.mark.local
def test_send_token6(
    app: Web3CliTest,
    alice: Account,
    bob: Account,
    token6: BrownieContract,
) -> None:
    bob_balance = token6.balanceOf(bob.address)
    seed_local_token(app, token6)
    app.set_args(
        ["--signer", "alice", "send", bob.address, "1", token6.symbol(), "--force"]
    ).run()
    assert token6.balanceOf(bob.address) == bob_balance + 10**6


@pytest.mark.local
def test_send_token6_smallest(
    app: Web3CliTest,
    alice: Account,
    bob: Account,
    token6: BrownieContract,
) -> None:
    bob_balance = token6.balanceOf(bob.address)
    seed_local_token(app, token6)
    app.set_args(
        [
            "--signer",
            "alice",
            "send",
            bob.address,
            "1",
            token6.symbol(),
            "smallest",
            "--force",
        ]
    ).run()
    assert token6.balanceOf(bob.address) == bob_balance + 1
