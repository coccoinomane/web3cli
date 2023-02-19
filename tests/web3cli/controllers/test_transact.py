from typing import Any, List

import pytest

from brownie.network.account import Account as BrownieAccount
from brownie.network.contract import Contract as BrownieContract
from tests.seed import seed_local_token
from tests.web3cli.main import Web3CliTest
from web3cli.exceptions import Web3CliError


@pytest.mark.local
@pytest.mark.parametrize(
    "args, error, error_message",
    [
        (
            [
                "transact",
                "tst18",
                "non_existing_function",
            ],
            Web3CliError,
            "Function must be one of",
        ),
        (
            [
                "transact",
                "tst18",
                "transfer",
                "0x123",
            ],
            Web3CliError,
            "Function transfer expects 2 arguments",
        ),
        (
            [
                "transact",
                "tst18",
                "transfer",
                "0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae",
                "should_be_an_int",
            ],
            ValueError,
            "String 'should_be_an_int' cannot be converted to a number",
        ),
        (
            [
                "transact",
                "tst18",
                "transfer",
                "bob",
                "1e18",
                "--no-call",
            ],
            Web3CliError,
            "Specify a gas limit",
        ),
    ],
)
# Test that providing a non existing function or
# wrong args to an existing function fails
def test_transact_invalid_input(
    app: Web3CliTest,
    token18: BrownieContract,
    alice: BrownieAccount,
    bob: BrownieAccount,
    args: List[str],
    error: Any,
    error_message: Any,
) -> None:
    seed_local_token(app, token18)
    with pytest.raises(error, match=error_message):
        app.set_args(
            [
                "--signer",
                "alice",
            ]
            + args
            + ["--force"]
        ).run()


@pytest.mark.local
@pytest.mark.parametrize("dry_run", [True, False])
# Test executing the 'trasfer' on the local chain,
# with and without the --dry-run flag
def test_transact(
    app: Web3CliTest,
    token18: BrownieContract,
    alice: BrownieAccount,
    bob: BrownieAccount,
    dry_run: bool,
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
        ]
        + (["--dry-run"] if dry_run else ["--force"])
    ).run()
    if dry_run:
        assert token18.balanceOf(bob.address) == bob_balance
    else:
        assert token18.balanceOf(bob.address) == bob_balance + 1e18
    data, output = app.last_rendered
    assert type(data) is str
    assert data.startswith("0x")


@pytest.mark.local
@pytest.mark.parametrize("answer", ["yes", "no"])
# Test that the confirmation prompt works as intended
def test_transact_with_confirm(
    app: Web3CliTest,
    token18: BrownieContract,
    alice: BrownieAccount,
    bob: BrownieAccount,
    monkeypatch: pytest.MonkeyPatch,
    answer: str,
) -> None:
    seed_local_token(app, token18)
    bob_balance = token18.balanceOf(bob.address)
    args = [
        "--signer",
        "alice",
        "transact",
        "tst18",
        "transfer",
        "bob",
        "1e18",
    ]
    monkeypatch.setattr("builtins.input", lambda _: answer)
    if answer == "yes":
        app.set_args(args).run()
        assert token18.balanceOf(bob.address) == bob_balance + 1e18
    else:
        with pytest.raises(SystemExit):
            app.set_args(args).run()
            assert token18.balanceOf(bob.address) == bob_balance


@pytest.mark.local
@pytest.mark.parametrize(
    "return_, has_keys",
    [
        (
            "params",
            [
                "to",
                "data",
                "value",
                "gas",
                "nonce",
                "chainId",
            ],
        ),
        (
            "sig",
            [
                "rawTransaction",
                "hash",
                "r",
                "s",
                "v",
            ],
        ),
        (
            "data",
            [
                "blockNumber",
                "blockHash",
                "gas",
            ],
        ),
        (
            "receipt",
            [
                "blockHash",
                "blockNumber",
                "logs",
                "gasUsed",
            ],
        ),
        (
            "all",
            [
                "params",
                "hash",
                "sig",
                "output",
                "data",
                "receipt",
            ],
        ),
    ],
)
# Test that varying the --return parameter the output varies
def test_transact_return(
    app: Web3CliTest,
    token18: BrownieContract,
    alice: BrownieAccount,
    bob: BrownieAccount,
    return_: str,
    has_keys: List[str],
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
            "--return",
            return_,
            "--force",
        ]
    ).run()
    assert token18.balanceOf(bob.address) == bob_balance + 1e18
    data, output = app.last_rendered
    assert type(data) is dict
    for key in has_keys:
        assert key in data


@pytest.mark.local
@pytest.mark.parametrize("dry_run", [True, False])
# Test that the function's output is printed when --return=output is used,
# regardless of whether we are in dry-run mode or not
def test_transact_return_output(
    app: Web3CliTest,
    token18: BrownieContract,
    alice: BrownieAccount,
    bob: BrownieAccount,
    dry_run: bool,
) -> None:
    seed_local_token(app, token18)
    app.set_args(
        [
            "--signer",
            "alice",
            "transact",
            "tst18",
            "transfer",
            "bob",
            "1e18",
            "--return",
            "output",
        ]
        + (["--dry-run"] if dry_run else ["--force"])
    ).run()
    data, output = app.last_rendered
    assert type(data) is bool
    assert data == True


@pytest.mark.local
@pytest.mark.parametrize("return_type", ["data", "receipt"])
# Test that an error is thrown when --return=receipt or --return=data
# is used in a dry run
def test_transact_output_receipt_dry_run(
    app: Web3CliTest,
    token18: BrownieContract,
    alice: BrownieAccount,
    bob: BrownieAccount,
    return_type: str,
) -> None:
    seed_local_token(app, token18)
    with pytest.raises(
        Web3CliError, match=f"Cannot return '{return_type}' with 'dry_run' option"
    ):
        app.set_args(
            [
                "--signer",
                "alice",
                "transact",
                "tst18",
                "transfer",
                "bob",
                "1e18",
                "--return",
                return_type,
                "--force",
                "--dry-run",
            ]
        ).run()


@pytest.mark.local
@pytest.mark.parametrize("call", [True, False])
# Test that executing the 'trasfer' on the local chain, with and without the
# --no-call flag, will always result in the transaction being executed. The
# difference is that when --no-call is used, the output of the function is not
# available in the output when --return=all is used. Also tests that the default
# is --call
def test_transact_call(
    app: Web3CliTest,
    token18: BrownieContract,
    alice: BrownieAccount,
    bob: BrownieAccount,
    call: bool,
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
            "--return",
            "all",
            "--force",
        ]
        + (["--no-call", "--gas-limit", "300000"] if not call else [])
    ).run()
    assert token18.balanceOf(bob.address) == bob_balance + 1e18
    data, output = app.last_rendered
    assert "output" in data
    if call:
        # If we are calling the function, the output should be populated
        assert type(data["output"]) is bool
        assert data["output"] == True
    else:
        # If we are not calling the function, the output should be empty
        assert data["output"] is None

    # The receipt should always be populated because we are not in dry-run mode
    assert "receipt" in data
    assert type(data["receipt"]) is dict
    assert "logs" in data["receipt"]


@pytest.mark.local
# Test that the gas_limit is correctly passed to the transaction
def test_transact_call_with_gas_limit(
    app: Web3CliTest,
    token18: BrownieContract,
    alice: BrownieAccount,
    bob: BrownieAccount,
) -> None:
    seed_local_token(app, token18)
    bob_balance = token18.balanceOf(bob.address)
    gas_limit = 300000
    app.set_args(
        [
            "--signer",
            "alice",
            "transact",
            "tst18",
            "transfer",
            "bob",
            "1e18",
            "--gas-limit",
            str(gas_limit),
            "--return",
            "data",
            "--force",
        ]
    ).run()
    assert token18.balanceOf(bob.address) == bob_balance + 1e18
    data, output = app.last_rendered
    assert "gas" in data
    assert type(data["gas"]) is int
    assert data["gas"] == gas_limit
