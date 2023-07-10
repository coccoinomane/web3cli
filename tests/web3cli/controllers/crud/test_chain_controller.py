from typing import List

import pytest

from tests.web3cli.main import Web3CliTest
from web3cli.exceptions import Web3CliError
from web3core.exceptions import RecordNotFound
from web3core.helpers.seed import seed_chains
from web3core.models.chain import Chain
from web3core.models.types import ChainFields


def test_chain_list(chains: List[ChainFields]) -> None:
    with Web3CliTest() as app:
        seed_chains(chains)
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
            "--desc",
            str(c["desc"]),
        ]
        if "geth_poa_middleware" in c["middlewares"]:
            argv.append("--poa")
        with Web3CliTest() as app:
            app.set_args(argv).run()
            assert Chain.select().count() == 1
            chain: Chain = Chain.get_by_name(c["name"])
            assert chain.chain_id == c["chain_id"]
            assert chain.coin == c["coin"]
            assert chain.desc == c["desc"]
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
    for chain in chains:
        with Web3CliTest() as app:
            seed_chains(chains)
            app.set_args(["chain", "get", chain["name"]]).run()
            data, output = app.last_rendered
            assert data["name"] == chain["name"]
            assert data["chain_id"] == chain["chain_id"]
            assert data["coin"] == chain["coin"]
            assert data["tx_type"] == chain["tx_type"]
            assert data["desc"] == chain["desc"]
            assert data["middlewares"] == chain["middlewares"]


def test_chain_active(chains: List[ChainFields]) -> None:
    for chain in chains:
        with Web3CliTest() as app:
            seed_chains(chains)
            app.set_option("default_chain", chain["name"])
            app.set_args(["chain", "active"]).run()
            data, output = app.last_rendered
            assert data == chain["name"]


def test_chain_delete(chains: List[ChainFields]) -> None:
    for c in chains:
        with Web3CliTest() as app:
            seed_chains(chains)
            app.set_args(
                [
                    "chain",
                    "delete",
                    c["name"],
                ]
            ).run()
            assert Chain.select().count() == len(chains) - 1
            with pytest.raises(RecordNotFound):
                Chain.get_by_name_or_raise(c["name"])
