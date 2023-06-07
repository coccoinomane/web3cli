import pytest

import ape
from tests.web3cli.main import Web3CliTest


@pytest.mark.local
def test_replay(
    app: Web3CliTest, alice: ape.api.AccountAPI, bob: ape.api.AccountAPI
) -> None:
    bob_balance = bob.balance
    original_tx = alice.transfer(bob, 10000)
    assert bob.balance == bob_balance + 10000
    app.set_args(
        [
            "replay",
            str(original_tx.txn_hash),
            "--gas-multiplier",
            "1",
            "-s",
            "alice",
            "--force",
        ]
    ).run()
    assert bob.balance == bob_balance + 20000


@pytest.mark.local
def test_replay_contract_tx(
    app: Web3CliTest,
    alice: ape.api.AccountAPI,
    bob: ape.api.AccountAPI,
    TST: ape.contracts.ContractInstance,
) -> None:
    bob_balance = TST.balanceOf(bob.address)
    original_tx = TST.transfer(bob, 10000, sender=alice)
    assert TST.balanceOf(bob.address) == bob_balance + 10000
    app.set_args(
        [
            "replay",
            str(original_tx.txn_hash),
            "--gas-multiplier",
            "1",
            "-s",
            "alice",
            "--force",
        ]
    ).run()
    assert TST.balanceOf(bob.address) == bob_balance + 20000
