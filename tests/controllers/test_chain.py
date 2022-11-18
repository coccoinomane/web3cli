from tests.main import Web3CliTest
from typing import List
from web3cli.core.seeds.chains import seed_chains
from web3cli.core.models.chain import Chain


def test_chain_list() -> None:
    with Web3CliTest() as app:
        Chain.seed(seed_chains)
        app.set_args(["chain", "list"]).run()
        data, output = app.last_rendered
        assert "ethereum" in output


def test_chain_get(app: Web3CliTest, chains: List[str]) -> None:
    """With explicit argument > return argument value"""
    for chain in chains:
        with Web3CliTest() as app:
            app.set_args(["--chain", chain, "chain", "get"]).run()
            data, output = app.last_rendered
            assert data["out"] == chain


def test_chain_get_no_args(app: Web3CliTest, chains: List[str]) -> None:
    """Without any argument > return the default chain"""
    for chain in chains:
        with Web3CliTest() as app:
            app.config.set("web3cli", "default_chain", chain)
            app.set_args(["chain", "get"]).run()
            data, output = app.last_rendered
            assert data["out"] == chain
