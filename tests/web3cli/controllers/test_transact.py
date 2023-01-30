import pytest

from brownie.network.account import Account as BrownieAccount
from brownie.network.contract import Contract as BrownieContract
from tests.seed import seed_local_token
from tests.web3cli.main import Web3CliTest
from web3cli.exceptions import Web3CliError


@pytest.mark.local
# Test that executing a non existing function fails with a Web3CliError
# exception containing the string "Function must be one..."
def test_transact_non_existing_function(
    app: Web3CliTest,
    token18: BrownieContract,
    alice: BrownieAccount,
    bob: BrownieAccount,
) -> None:
    seed_local_token(app, token18)
    with pytest.raises(Web3CliError, match="Function must be one of"):
        app.set_args(
            [
                "--signer",
                "alice",
                "transact",
                "tst18",
                "non_existing_function",
                "--force",
            ]
        ).run()


@pytest.mark.local
# Test that executing a function with the wrong number of arguments fails
def test_transact_wrong_number_of_arguments(
    app: Web3CliTest,
    token18: BrownieContract,
    alice: BrownieAccount,
    bob: BrownieAccount,
) -> None:
    seed_local_token(app, token18)
    with pytest.raises(Web3CliError, match="Function transfer expects 2 arguments"):
        app.set_args(
            [
                "--signer",
                "alice",
                "transact",
                "tst18",
                "transfer",
                "0x123",
                "--force",
            ]
        ).run()


@pytest.mark.local
# Test that executing a function with the wrong type of arguments fails
def test_transact_wrong_type_of_arguments(
    app: Web3CliTest,
    token18: BrownieContract,
    alice: BrownieAccount,
    bob: BrownieAccount,
) -> None:
    seed_local_token(app, token18)
    with pytest.raises(ValueError):
        app.set_args(
            [
                "--signer",
                "alice",
                "transact",
                "tst18",
                "transfer",
                "0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae",
                "should_be_an_int",
                "--force",
            ]
        ).run()


@pytest.mark.local
# Test executing the 'trasfer' function on the TST18 token on the local chain
def test_transact_local_token_transfer(
    app: Web3CliTest,
    token18: BrownieContract,
    alice: BrownieAccount,
    bob: BrownieAccount,
) -> None:
    seed_local_token(app, token18)
    bob_balance = token18.balanceOf(bob.address)
    app.set_args(
        [
            "--signer",
            "alice",
            "transact",
            "tst18",
            "transfer",
            "bob",
            "1e18",
            "--force",
        ]
    ).run()
    assert token18.balanceOf(bob.address) == bob_balance + 1e18
    data, output = app.last_rendered
    assert type(data) is str
    assert data.startswith("0x")


@pytest.mark.local
# Test that excution continues if the user does confirm
def test_transact_local_token_transfer_with_confirm(
    app: Web3CliTest,
    token18: BrownieContract,
    alice: BrownieAccount,
    bob: BrownieAccount,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    seed_local_token(app, token18)
    bob_balance = token18.balanceOf(bob.address)
    monkeypatch.setattr("builtins.input", lambda _: "yes")
    app.set_args(
        [
            "--signer",
            "alice",
            "transact",
            "tst18",
            "transfer",
            "bob",
            "1e18",
        ]
    ).run()
    assert token18.balanceOf(bob.address) == bob_balance + 1e18


@pytest.mark.local
# Test that excution stops if the user does not confirm
def test_transact_local_token_transfer_no_confirm(
    app: Web3CliTest,
    token18: BrownieContract,
    alice: BrownieAccount,
    bob: BrownieAccount,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    seed_local_token(app, token18)
    bob_balance = token18.balanceOf(bob.address)
    monkeypatch.setattr("builtins.input", lambda _: "no")
    with pytest.raises(SystemExit):
        app.set_args(
            [
                "--signer",
                "alice",
                "transact",
                "tst18",
                "transfer",
                "bob",
                "1e18",
            ]
        ).run()
    assert token18.balanceOf(bob.address) == bob_balance


@pytest.mark.local
# Test that execution stops when --dry-run is used
def test_transact_local_token_transfer_dry_run(
    app: Web3CliTest,
    token18: BrownieContract,
    alice: BrownieAccount,
    bob: BrownieAccount,
) -> None:
    seed_local_token(app, token18)
    bob_balance = token18.balanceOf(bob.address)
    app.set_args(
        [
            "--signer",
            "alice",
            "transact",
            "tst18",
            "transfer",
            "bob",
            "1e18",
            "--dry-run",
        ]
    ).run()
    assert token18.balanceOf(bob.address) == bob_balance


@pytest.mark.local
# Test that the transaction JSON is printed when --output=tx is used
def test_transact_local_token_transfer_output_tx(
    app: Web3CliTest,
    token18: BrownieContract,
    alice: BrownieAccount,
    bob: BrownieAccount,
) -> None:
    seed_local_token(app, token18)
    bob_balance = token18.balanceOf(bob.address)
    app.set_args(
        [
            "--signer",
            "alice",
            "transact",
            "tst18",
            "transfer",
            "bob",
            "1e18",
            "--output",
            "tx",
            "--force",
        ]
    ).run()
    assert token18.balanceOf(bob.address) == bob_balance + 1e18
    data, output = app.last_rendered
    assert type(data) is dict
    assert "to" in data
    assert "data" in data
    assert "value" in data
    assert "gas" in data
    assert "nonce" in data
    assert "chainId" in data


@pytest.mark.local
# Test that the signed transaction JSON is printed when --output=sig is used
def test_transact_local_token_transfer_output_sig(
    app: Web3CliTest,
    token18: BrownieContract,
    alice: BrownieAccount,
    bob: BrownieAccount,
) -> None:
    seed_local_token(app, token18)
    bob_balance = token18.balanceOf(bob.address)
    app.set_args(
        [
            "--signer",
            "alice",
            "transact",
            "tst18",
            "transfer",
            "bob",
            "1e18",
            "--output",
            "sig",
            "--force",
        ]
    ).run()
    assert token18.balanceOf(bob.address) == bob_balance + 1e18
    data, output = app.last_rendered
    assert type(data) is dict
    assert "rawTransaction" in data
    assert "hash" in data
    assert "r" in data
    assert "s" in data
    assert "v" in data


@pytest.mark.local
# Test that the transaction receipt JSON is printed when --output=receipt is
# used
def test_transact_local_token_transfer_output_receipt(
    app: Web3CliTest,
    token18: BrownieContract,
    alice: BrownieAccount,
    bob: BrownieAccount,
) -> None:
    seed_local_token(app, token18)
    bob_balance = token18.balanceOf(bob.address)
    app.set_args(
        [
            "--signer",
            "alice",
            "transact",
            "tst18",
            "transfer",
            "bob",
            "1e18",
            "--output",
            "receipt",
            "--force",
        ]
    ).run()
    assert token18.balanceOf(bob.address) == bob_balance + 1e18
    data, output = app.last_rendered
    assert type(data) is dict
    assert "blockHash" in data
    assert "blockNumber" in data
    assert "logs" in data
