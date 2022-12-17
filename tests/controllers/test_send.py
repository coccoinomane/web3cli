from typing import Any, Dict, List

import pytest
from brownie.network.account import Account
from brownie.network.state import TxHistory

from tests.main import Web3CliTest
from web3cli.core.models.types import ChainFields
from web3cli.helpers.seed import seed_chains, seed_signers


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
    ## When we will understand how to access tx history:
    # data, output = app.last_rendered
    # assert len(history) == 1
    # assert output == history[0].txid
    ## When we will be able to get gas fee from history
    # assert alice.balance() == alice_balance - 1000000000000000000 - history[0].gas_fee
    ## When we will be using london hardfork in ganache:
    # assert history[0].priority_fee == app.priority_fee


@pytest.mark.local
def test_send_eth_wei(app: Web3CliTest, alice: Account, bob: Account) -> None:
    bob_balance = bob.balance()
    app.set_args(
        ["--signer", "alice", "send", bob.address, "1", "ETH", "wei", "--force"]
    ).run()
    assert bob.balance() == bob_balance + 1
