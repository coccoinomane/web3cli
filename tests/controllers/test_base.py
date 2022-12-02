from typing import Any, Dict, List
from tests.main import Web3CliTest
import pytest
from tests.seeder import seed_chains, seed_signers
from web3cli.core.models.types import ChainFields
from web3cli.helpers.misc import get_coin
from brownie.network.account import Account
from brownie.network.state import TxHistory


@pytest.mark.slow
def test_balance(chains: List[ChainFields]) -> None:
    with Web3CliTest() as app:
        seed_chains(app, chains)
        app.set_args(["balance", "0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae"]).run()
        data, output = app.last_rendered
        assert type(data["amount"]) is float
        assert data["amount"] >= 0
        assert data["ticker"] == get_coin(app)


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


@pytest.mark.parametrize(
    "msg",
    [
        "Hello world!",
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam pulvinar lacus erat, et sollicitudin purus rutrum sed. Aliquam pulvinar nunc nec sagittis sagittis. Nunc efficitur lacus urna, sed dapibus lacus varius id. Nam laoreet convallis nisl, ut lacinia sem congue eu. Phasellus eu nisi in lectus lobortis viverra a at diam. Nulla dolor nisl, mollis efficitur venenatis in, elementum consequat quam. Sed a euismod justo, quis maximus velit. Maecenas varius augue dolor, sit amet elementum lacus pretium vitae. Fusce egestas condimentum quam eget elementum. Suspendisse vulputate ut urna a pretium. Nunc semper a sem fermentum dapibus.",
        "I will copiously donate to coccoinomane ❤️",
    ],
)
def test_sign(
    msg: str, signers: List[Dict[str, Any]], chains: List[ChainFields]
) -> None:
    with Web3CliTest() as app:
        seed_chains(app, chains)
        seed_signers(app, [signers[0]])
        app.set_args(["sign", msg]).run()
        data, output = app.last_rendered
        assert "messageHash" in data["out"]
        assert "r" in data["out"]
        assert "s" in data["out"]
        assert "v" in data["out"]
        assert "signature" in data["out"]
