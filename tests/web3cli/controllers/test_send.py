from typing import Any, Dict, List

import pytest
from brownie.network.account import Account
from brownie.network.state import TxHistory

from tests.web3cli.main import Web3CliTest
from web3cli.helpers.seed import seed_chains, seed_signers
from web3core.models.types import ChainFields


@pytest.mark.local
def test_send_eth(
    app: Web3CliTest, alice: Account, bob: Account, history: TxHistory
) -> None:
    alice_balance = alice.balance()
    bob_balance = bob.balance()
    app.set_args(
        ["--signer", "alice", "send", bob.address, "1", "ETH", "--force"]
    ).run()
    assert bob.balance() == bob_balance + 1000000000000000000


@pytest.mark.local
def test_send_eth_wei(app: Web3CliTest, alice: Account, bob: Account) -> None:
    bob_balance = bob.balance()
    app.set_args(
        ["--signer", "alice", "send", bob.address, "1", "ETH", "wei", "--force"]
    ).run()
    assert bob.balance() == bob_balance + 1
