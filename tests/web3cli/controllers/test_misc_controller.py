import decimal
import json
from decimal import Decimal
from typing import Any, Dict, List

import pytest
from web3 import Web3

import ape
from tests.web3cli.main import Web3CliTest
from web3core.helpers.seed import seed_signers


@pytest.mark.local
def test_balance(
    app: Web3CliTest,
    alice: ape.api.AccountAPI,
    bob: ape.api.AccountAPI,
) -> None:
    alice_balance = alice.balance
    bob.transfer(alice, 10**18)
    app.set_args(["balance", alice.address]).run()
    data, output = app.last_rendered
    assert type(data) is Decimal
    assert data == Web3.from_wei(alice_balance + 10**18, "ether")


@pytest.mark.local
def test_balance_with_alias(
    app: Web3CliTest,
    alice: ape.api.AccountAPI,
    bob: ape.api.AccountAPI,
) -> None:
    alice_balance = alice.balance
    bob.transfer(alice, 10**18)
    app.set_args(["balance", "alice"]).run()  # use the alias
    data, output = app.last_rendered
    assert type(data) is Decimal
    assert data == Web3.from_wei(alice_balance + 10**18, "ether")


@pytest.mark.local
def test_balance_with_unit_gwei(
    app: Web3CliTest,
    alice: ape.api.AccountAPI,
    bob: ape.api.AccountAPI,
) -> None:
    alice_balance = alice.balance
    bob.transfer(alice, 10**18)
    app.set_args(["balance", alice.address, "-u", "gwei"]).run()
    data, output = app.last_rendered
    assert type(data) is Decimal
    assert data == Web3.from_wei(alice_balance + 10**18, "gwei")


@pytest.mark.local
def test_balance_with_unit_wei(
    app: Web3CliTest,
    alice: ape.api.AccountAPI,
    bob: ape.api.AccountAPI,
) -> None:
    alice_balance = alice.balance
    bob.transfer(alice, 10**18)
    app.set_args(["balance", alice.address, "-u", "wei"]).run()
    data, output = app.last_rendered
    assert type(data) is int
    assert data == alice_balance + 10**18


@pytest.mark.local
def test_tx_count(
    app: Web3CliTest,
    alice: ape.api.AccountAPI,
    bob: ape.api.AccountAPI,
    ape_chain: ape.managers.chain.ChainManager,
) -> None:
    alice.transfer(bob, 10000)
    alice.transfer(bob, 20000)
    ape_chain.mine()
    alice.transfer(bob, 30000)
    app.set_args(["tx-count", "alice"]).run()
    data, output = app.last_rendered
    assert type(data) is int
    assert data == 3


@pytest.mark.parametrize(
    "msg",
    [
        "Hello world!",
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam pulvinar lacus erat, et sollicitudin purus rutrum sed. Aliquam pulvinar nunc nec sagittis sagittis. Nunc efficitur lacus urna, sed dapibus lacus varius id. Nam laoreet convallis nisl, ut lacinia sem congue eu. Phasellus eu nisi in lectus lobortis viverra a at diam. Nulla dolor nisl, mollis efficitur venenatis in, elementum consequat quam. Sed a euismod justo, quis maximus velit. Maecenas varius augue dolor, sit amet elementum lacus pretium vitae. Fusce egestas condimentum quam eget elementum. Suspendisse vulputate ut urna a pretium. Nunc semper a sem fermentum dapibus.",
        "I will copiously donate to coccoinomane",
    ],
)
def test_sign(msg: str, signers: List[Dict[str, Any]]) -> None:
    with Web3CliTest() as app:
        seed_signers([signers[0]], app.app_key)
        app.set_args(["sign", msg]).run()
        data, output = app.last_rendered
        assert "messageHash" in data
        assert "r" in data
        assert "s" in data
        assert "v" in data
        assert "signature" in data


@pytest.mark.local
def test_block_latest(
    app: Web3CliTest, alice: ape.api.AccountAPI, bob: ape.api.AccountAPI
) -> None:
    tx = alice.transfer(bob, 10000)
    app.set_args(["block", "latest"]).run()
    data, output = app.last_rendered
    block: dict[str, Any] = json.loads(output)
    assert type(block.get("transactions")) == list
    assert len(block["transactions"]) == 1
    assert block["transactions"][0] == tx.txn_hash


@pytest.mark.local
def test_block_number(
    app: Web3CliTest,
    alice: ape.api.AccountAPI,
    bob: ape.api.AccountAPI,
    ape_chain: ape.managers.chain.ChainManager,
) -> None:
    initial_height = ape_chain.blocks.height
    tx = alice.transfer(bob, 10000)
    ape_chain.mine()
    app.set_args(["block", str(initial_height + 1)]).run()
    data, output = app.last_rendered
    block: dict[str, Any] = json.loads(output)
    assert type(block.get("transactions")) == list
    assert len(block["transactions"]) == 1
    assert block["transactions"][0] == tx.txn_hash


@pytest.mark.local
def test_block_hash(
    app: Web3CliTest,
    alice: ape.api.AccountAPI,
    bob: ape.api.AccountAPI,
    ape_chain: ape.managers.chain.ChainManager,
) -> None:
    # Make a transaction (+1 height) then mine a block (+1 height)
    initial_height = ape_chain.blocks.height
    tx = alice.transfer(bob, 10000)
    ape_chain.mine()
    # Retrieve hash of transaction block
    hash = ape_chain.blocks[initial_height + 1].hash.hex()
    # Retrieve transaction block by hash using the CLI
    app.set_args(["block", hash]).run()
    data, output = app.last_rendered
    block: dict[str, Any] = json.loads(output)
    assert type(block.get("transactions")) == list
    assert len(block["transactions"]) == 1
    assert block["transactions"][0] == tx.txn_hash


@pytest.mark.local
def test_gas_price(app: Web3CliTest, is_eip1559: bool) -> None:
    if is_eip1559:
        pytest.skip("Local chain does not have gas price")
    app.set_args(["gas-price"]).run()
    data, output = app.last_rendered
    assert type(data) is float
    assert data > 0


@pytest.mark.local
def test_base_fee(app: Web3CliTest, is_eip1559: bool) -> None:
    if not is_eip1559:
        pytest.skip("Local chain does not have base fee")
    app.set_args(["base-fee"]).run()
    data, output = app.last_rendered
    assert type(data) in (decimal.Decimal, int, float)
    assert data >= 0
