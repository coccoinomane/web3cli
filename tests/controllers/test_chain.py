from tests.main import Web3CliTest
from typing import List
from tests.seeder import seed_chains
from web3cli.core.exceptions import Web3CliError
from web3cli.core.models.chain import Chain
import pytest
from web3cli.core.models.types import ChainFields


def test_chain_list(chains: List[ChainFields]) -> None:
    with Web3CliTest() as app:
        seed_chains(app, chains)
        app.set_args(["chain", "list"]).run()
        data, output = app.last_rendered
        for c in chains:
            assert c["name"] in output
            assert c["coin"] in output


def test_chain_add(chains: List[ChainFields]) -> None:
    for c in chains:
        # Add the chain > ok!
        argv = [
            "chain",
            "add",
            c["name"],
            str(c["chain_id"]),
            c["coin"],
            "--tx-type",
            str(c["tx_type"]),
        ]
        if "geth_poa_middleware" in c["middlewares"]:
            argv.append("--poa")
        with Web3CliTest() as app:
            app.set_args(argv).run()
            assert Chain.select().count() == 1
            chain: Chain = Chain.get_by_name(c["name"])
            assert chain.chain_id == c["chain_id"]
            assert chain.coin == c["coin"]
        # Add the chain again > exception!
        with Web3CliTest(delete_db=False) as app:
            with pytest.raises(Web3CliError, match=r"already exists"):
                app.set_args(argv).run()
        # Add the chain again with --update option > ok!
        with Web3CliTest(delete_db=False) as app:
            updated_argv = argv + ["--update"]
            updated_argv[4] = f"{c['coin']}_UPDATED"
            print(updated_argv)
            app.set_args(updated_argv).run()
            assert Chain.select().count() == 1
            updated_chain: Chain = Chain.get_by_name(c["name"])
            assert updated_chain.chain_id == c["chain_id"]
            assert updated_chain.coin == updated_argv[4]


def test_chain_get(chains: List[ChainFields]) -> None:
    """With explicit argument > return argument value"""
    for chain in chains:
        with Web3CliTest() as app:
            seed_chains(app, chains)
            app.set_args(["--chain", chain["name"], "chain", "get"]).run()
            data, output = app.last_rendered
            assert data["out"] == chain["name"]


def test_chain_get_no_args(chains: List[ChainFields]) -> None:
    """Without any argument > return the default chain"""
    for chain in chains:
        with Web3CliTest() as app:
            seed_chains(app, chains)
            app.config.set("web3cli", "default_chain", chain["name"])
            app.set_args(["chain", "get"]).run()
            data, output = app.last_rendered
            assert data["out"] == chain["name"]


def test_chain_delete(chains: List[ChainFields]) -> None:
    for c in chains:
        with Web3CliTest() as app:
            seed_chains(app, chains)
            app.set_args(
                [
                    "chain",
                    "delete",
                    c["name"],
                ]
            ).run()
            assert Chain.select().count() == len(chains) - 1
