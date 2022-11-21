from tests.main import Web3CliTest
from typing import List
from tests.seeder import seed_chains
from web3cli.core.seeds.types import ChainSeed


def test_chain_list(chains: List[ChainSeed]) -> None:
    with Web3CliTest() as app:
        seed_chains(app, chains)
        app.set_args(["chain", "list"]).run()
        data, output = app.last_rendered
        assert "ethereum" in output


def test_chain_get(chains: List[ChainSeed]) -> None:
    """With explicit argument > return argument value"""
    for chain in chains:
        with Web3CliTest() as app:
            seed_chains(app, chains)
            app.set_args(["--chain", chain["name"], "chain", "get"]).run()
            data, output = app.last_rendered
            assert data["out"] == chain["name"]


def test_chain_get_no_args(chains: List[ChainSeed]) -> None:
    """Without any argument > return the default chain"""
    for chain in chains:
        with Web3CliTest() as app:
            seed_chains(app, chains)
            app.config.set("web3cli", "default_chain", chain["name"])
            app.set_args(["chain", "get"]).run()
            data, output = app.last_rendered
            assert data["out"] == chain["name"]
