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
        ]
    ).run()
    assert token18.balanceOf(bob.address) == bob_balance + 1e18
