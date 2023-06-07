import json
from typing import Any

import pytest

import ape
from tests.web3cli.main import Web3CliTest


@pytest.mark.local
def test_tx_get(
    app: Web3CliTest, alice: ape.api.AccountAPI, bob: ape.api.AccountAPI
) -> None:
    value = 10000
    sent_tx = alice.transfer(bob, value)
    app.set_args(["tx", "get", str(sent_tx.txn_hash)]).run()
    data, output = app.last_rendered
    tx: dict[str, Any] = json.loads(output)
    assert tx.get("hash") == sent_tx.txn_hash
    assert tx.get("value") == value
    assert tx.get("from") == alice.address
    assert tx.get("to") == bob.address
    assert type(tx.get("v")) == int
    assert type(tx.get("r")) == str
    assert type(tx.get("s")) == str


@pytest.mark.local
def test_tx_get_receipt(
    app: Web3CliTest, alice: ape.api.AccountAPI, bob: ape.api.AccountAPI
) -> None:
    sent_tx = alice.transfer(bob, 10000)
    app.set_args(["tx", "get-receipt", str(sent_tx.txn_hash)]).run()
    data, output = app.last_rendered
    receipt: dict[str, Any] = json.loads(output)
    assert receipt.get("transactionHash") == sent_tx.txn_hash
    assert receipt.get("from") == alice.address
    assert receipt.get("to") == bob.address
    assert type(receipt.get("gasUsed")) == int
    assert receipt.get("gasUsed") > 0


@pytest.mark.local
def test_tx_replay(
    app: Web3CliTest, alice: ape.api.AccountAPI, bob: ape.api.AccountAPI
) -> None:
    bob_balance = bob.balance
    original_tx = alice.transfer(bob, 10000)
    assert bob.balance == bob_balance + 10000
    app.set_args(
        [
            "tx",
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
def test_tx_replay_contract_tx(
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
            "tx",
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
