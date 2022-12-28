import json
from typing import Any, Dict, List

import pytest
from brownie.network.account import Account

from tests.web3cli.main import Web3CliTest
from web3cli.helpers.seed import seed_chains, seed_signers
from web3core.models.types import ChainFields


@pytest.mark.slow
def test_balance(chains: List[ChainFields]) -> None:
    with Web3CliTest() as app:
        seed_chains(app, chains)
        app.set_args(["balance", "0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae"]).run()
        data, output = app.last_rendered
        assert type(data["amount"]) is float
        assert data["amount"] >= 0
        assert data["ticker"] == app.chain.coin


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


@pytest.mark.local
def test_block(app: Web3CliTest, alice: Account, bob: Account) -> None:
    tx = alice.transfer(bob, 10000)
    app.set_args(["block", "latest"]).run()
    data, output = app.last_rendered
    block: dict[str, Any] = json.loads(output)
    assert type(block.get("transactions")) == list
    assert len(block["transactions"]) == 1
    assert block["transactions"][0] == tx.txid
