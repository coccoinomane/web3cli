import pytest

import ape
from tests.seed import seed_local_token
from tests.web3cli.main import Web3CliTest


@pytest.mark.local
def test_send_eth(
    app: Web3CliTest, alice: ape.api.AccountAPI, bob: ape.api.AccountAPI
) -> None:
    bob_balance = bob.balance
    app.set_args(
        ["send", bob.address, "1", "ETH", "--force", "--signer", "alice"]
    ).run()
    assert bob.balance == bob_balance + 10**18


@pytest.mark.local
def test_send_eth_using_address_tag(
    app: Web3CliTest, alice: ape.api.AccountAPI, bob: ape.api.AccountAPI
) -> None:
    bob_balance = bob.balance
    app.set_args(["send", "bob", "1", "ETH", "--signer", "alice", "--force"]).run()
    assert bob.balance == bob_balance + 10**18


@pytest.mark.local
def test_send_eth_wei(
    app: Web3CliTest, alice: ape.api.AccountAPI, bob: ape.api.AccountAPI
) -> None:
    bob_balance = bob.balance
    app.set_args(
        ["send", bob.address, "1", "ETH", "wei", "--signer", "alice", "--force"]
    ).run()
    assert bob.balance == bob_balance + 1


@pytest.mark.local
def test_send_token(
    app: Web3CliTest,
    alice: ape.api.AccountAPI,
    bob: ape.api.AccountAPI,
    TST: ape.contracts.ContractInstance,
) -> None:
    bob_balance = TST.balanceOf(bob.address)
    seed_local_token(app, TST)
    app.set_args(
        ["send", bob.address, "1", TST.symbol(), "--signer", "alice", "--force"]
    ).run()
    assert TST.balanceOf(bob.address) == bob_balance + 10**18


@pytest.mark.local
def test_send_token_with_alias(
    app: Web3CliTest,
    alice: ape.api.AccountAPI,
    bob: ape.api.AccountAPI,
    TST: ape.contracts.ContractInstance,
) -> None:
    bob_balance = TST.balanceOf(bob.address)
    seed_local_token(app, TST)
    app.set_args(
        ["send", "bob", "1", TST.symbol(), "--signer", "alice", "--force"]
    ).run()
    assert TST.balanceOf(bob.address) == bob_balance + 10**18


@pytest.mark.local
def test_send_token_smallest(
    app: Web3CliTest,
    alice: ape.api.AccountAPI,
    bob: ape.api.AccountAPI,
    TST: ape.contracts.ContractInstance,
) -> None:
    bob_balance = TST.balanceOf(bob.address)
    seed_local_token(app, TST)
    app.set_args(
        [
            "send",
            bob.address,
            "1",
            TST.symbol(),
            "smallest",
            "--signer",
            "alice",
            "--force",
        ]
    ).run()
    assert TST.balanceOf(bob.address) == bob_balance + 1


@pytest.mark.local
def test_send_token6(
    app: Web3CliTest,
    alice: ape.api.AccountAPI,
    bob: ape.api.AccountAPI,
    TST6: ape.contracts.ContractInstance,
) -> None:
    bob_balance = TST6.balanceOf(bob.address)
    seed_local_token(app, TST6)
    app.set_args(
        ["send", bob.address, "1", TST6.symbol(), "--signer", "alice", "--force"]
    ).run()
    assert TST6.balanceOf(bob.address) == bob_balance + 10**6


@pytest.mark.local
def test_send_token6_smallest(
    app: Web3CliTest,
    alice: ape.api.AccountAPI,
    bob: ape.api.AccountAPI,
    TST6: ape.contracts.ContractInstance,
) -> None:
    bob_balance = TST6.balanceOf(bob.address)
    seed_local_token(app, TST6)
    app.set_args(
        [
            "send",
            bob.address,
            "1",
            TST6.symbol(),
            "smallest",
            "--signer",
            "alice",
            "--force",
        ]
    ).run()
    assert TST6.balanceOf(bob.address) == bob_balance + 1
