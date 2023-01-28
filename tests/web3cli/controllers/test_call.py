from typing import List

import pytest

from tests.web3cli.main import Web3CliTest
from web3core.helpers.seed import seed_chains, seed_contracts
from web3core.models.types import ChainFields, ContractFields


@pytest.mark.remote
# Test calling the Uniswap Router V2 contract's getAmountsOut function
# (2 arguments of which one is an array)
def test_call_eth_uniswap_router_v2_get_amounts_out(
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
                "uniswap_router_v2",
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
        assert data[1] < 100e6


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
