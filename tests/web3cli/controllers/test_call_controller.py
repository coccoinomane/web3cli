from typing import List

import pytest

import ape
from tests.seed import seed_local_token
from tests.web3cli.main import Web3CliTest
from web3cli.exceptions import Web3CliError
from web3core.helpers.seed import seed_chains, seed_contracts
from web3core.models.types import ChainFields, ContractFields


@pytest.mark.local
# Test that calling a non existing function fails with a Web3CliError
# exception containing the string "Function must be one..."
def test_call_non_existing_function(
    app: Web3CliTest, TST: ape.contracts.ContractInstance
) -> None:
    seed_local_token(app, TST)
    with pytest.raises(Web3CliError, match="Function must be one of"):
        app.set_args(
            [
                "call",
                "tst",
                "non_existing_function",
            ]
        ).run()


@pytest.mark.local
# Test that calling a function with the wrong number of arguments fails
def test_call_wrong_number_of_arguments(
    app: Web3CliTest,
    TST: ape.contracts.ContractInstance,
    alice: ape.api.AccountAPI,
    bob: ape.api.AccountAPI,
) -> None:
    seed_local_token(app, TST)
    with pytest.raises(Web3CliError, match="Function transfer expects 2 arguments"):
        app.set_args(
            [
                "--signer",
                "alice",
                "call",
                "tst",
                "transfer",
                "0x123",
            ]
        ).run()


@pytest.mark.local
# Test that calling a function with the wrong type of arguments fails
def test_call_wrong_type_of_arguments(
    app: Web3CliTest,
    TST: ape.contracts.ContractInstance,
    alice: ape.api.AccountAPI,
    bob: ape.api.AccountAPI,
) -> None:
    seed_local_token(app, TST)
    with pytest.raises(ValueError):
        app.set_args(
            [
                "--signer",
                "alice",
                "call",
                "tst",
                "transfer",
                "0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae",
                "should_be_an_int",
            ]
        ).run()


@pytest.mark.local
# Test that calling a write function without neither a signer nor a from address fails
def test_call_local_token_transfer_without_signer_without_from(
    app: Web3CliTest,
    TST: ape.contracts.ContractInstance,
    alice: ape.api.AccountAPI,
    bob: ape.api.AccountAPI,
) -> None:
    seed_local_token(app, TST)
    TST.balanceOf(bob.address)
    with pytest.raises(
        Web3CliError, match="Cannot call a write operation without a from address"
    ):
        app.set_args(
            [
                "call",
                "tst",
                "transfer",
                "bob",
                "1e18",
            ]
        ).run()


@pytest.mark.local
# Test that calling a write function without a signer but with a from address
# works
def test_call_local_token_transfer_without_signer_with_from(
    app: Web3CliTest,
    TST: ape.contracts.ContractInstance,
    alice: ape.api.AccountAPI,
    bob: ape.api.AccountAPI,
) -> None:
    seed_local_token(app, TST)
    TST.balanceOf(bob.address)
    app.set_args(
        [
            "call",
            "tst",
            "transfer",
            "bob",
            "1e18",
            "--from",
            "alice",
        ]
    ).run()
    data, output = app.last_rendered
    assert output == "true"


@pytest.mark.local
# Test calling the 'trasfer' function on the TST token on the local chain
def test_call_local_token_transfer(
    app: Web3CliTest,
    TST: ape.contracts.ContractInstance,
    alice: ape.api.AccountAPI,
    bob: ape.api.AccountAPI,
) -> None:
    seed_local_token(app, TST)
    TST.balanceOf(bob.address)
    app.set_args(
        [
            "--signer",
            "alice",
            "call",
            "tst",
            "transfer",
            "bob",
            "1e18",
        ]
    ).run()
    data, output = app.last_rendered
    assert output == "true"


@pytest.mark.remote
# Test calling the Uniswap Router V2 contract's getAmountsOut function
# (2 arguments of which one is an array)
def test_call_eth_uniswap_v2_get_amounts_out(
    contracts: List[ContractFields], chains: List[ChainFields]
) -> None:
    with Web3CliTest() as app:
        seed_chains(chains)
        seed_contracts(contracts)
        app.set_args(
            [
                "-c",
                "eth",
                "call",
                "uniswap_v2",
                "getAmountsOut",
                "100e6",
                "usdc,usdt",
            ]
        ).run()
        data, output = app.last_rendered
        assert type(data) is list
        assert len(data) == 2
        assert type(data[0]) is int
        assert type(data[1]) is int
        assert data[0] == 100e6
        assert data[1] > 0


@pytest.mark.remote
# Test calling the WETH contract's totalSupply function
# (0 arguments)
def test_call_eth_weth_total_supply(
    contracts: List[ContractFields], chains: List[ChainFields]
) -> None:
    with Web3CliTest() as app:
        seed_chains(chains)
        seed_contracts(contracts)
        app.set_args(
            [
                "-c",
                "eth",
                "call",
                "weth",
                "totalSupply",
            ]
        ).run()
        data, output = app.last_rendered
        assert type(data) is int
        assert data > 1e18


@pytest.mark.remote
# Test calling the WETH contract's totalSupply function
# (two blocks ago)
def test_call_eth_weth_total_supply_two_blocks_ago(
    contracts: List[ContractFields], chains: List[ChainFields]
) -> None:
    with Web3CliTest() as app:
        seed_chains(chains)
        app.set_args(
            [
                "-c",
                "eth",
                "block",
                "latest",
            ]
        ).run()
        data, output = app.last_rendered
        latest = data["number"]

    with Web3CliTest() as app:
        seed_chains(chains)
        seed_contracts(contracts)
        app.set_args(
            [
                "-c",
                "eth",
                "call",
                "weth",
                "totalSupply",
                "--block",
                str(latest - 2),
            ]
        ).run()
        data, output = app.last_rendered
        assert type(data) is int
        assert data > 1e18


@pytest.mark.remote
# Test that calling a write function without a from address fails
def test_call_eth_weth_transfer_without_from_address(
    contracts: List[ContractFields], chains: List[ChainFields]
) -> None:
    with Web3CliTest() as app:
        seed_chains(chains)
        seed_contracts(contracts)
        with pytest.raises(
            Web3CliError, match="Cannot call a write operation without a from address"
        ):
            app.set_args(
                [
                    "-c",
                    "eth",
                    "call",
                    "weth",
                    "transfer",
                    "0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae",
                    "1e18",
                ]
            ).run()
