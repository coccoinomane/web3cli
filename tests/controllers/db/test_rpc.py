from tests.main import Web3CliTest
from typing import List
from tests.seeder import seed_chains
from web3cli.core.exceptions import RpcIsInvalid
from web3cli.core.models.chain import Chain, Rpc
import pytest
from web3cli.core.models.types import ChainFields


def test_rpc_list(chains: List[ChainFields]) -> None:
    with Web3CliTest() as app:
        seed_chains(app, chains)
        app.set_args(["db", "rpc", "list"]).run()
        data, output = app.last_rendered
        for c in chains:
            for r in c["rpcs"]:
                assert (
                    r["url"][0 : app.config.get("web3cli", "output_table_wrap")]
                    in output
                )


def test_rpc_add(chains: List[ChainFields]) -> None:
    c = chains[0]
    # Add two different RPCs > they should be in the DB
    test_rpcs = ["https://www.example-1.com", "https://www.example-2.com"]
    with Web3CliTest() as app:
        chain = Chain.create(name=c["name"], chain_id=c["chain_id"], coin=c["coin"])
        app.set_args(["db", "rpc", "add", chain.name] + test_rpcs).run()
        created_rpcs = chain.get_rpcs()
        assert len(created_rpcs) == len(test_rpcs)
        for i, rpc in enumerate(created_rpcs):
            assert rpc.url == test_rpcs[i]
    # Add the same RPCs again > they should not be added to the db
    with Web3CliTest(delete_db=False) as app:
        app.set_args(["db", "rpc", "add", chain.name] + test_rpcs).run()
        assert len(chain.get_rpcs()) == len(test_rpcs)
    # Add an RPC with a wrong URL > it should raise
    with Web3CliTest() as app:
        chain = Chain.create(name=c["name"], chain_id=c["chain_id"], coin=c["coin"])
        with pytest.raises(RpcIsInvalid):
            app.set_args(["db", "rpc", "add", chain.name, "not a URI"]).run()


def test_rpc_get_with_id_argument(chains: List[ChainFields]) -> None:
    """With ID argument > it should return the url of the RPC with given ID"""
    with Web3CliTest() as app:
        seed_chains(app, chains)
        rpcs = Rpc.get_all()
    for rpc in rpcs:
        with Web3CliTest(delete_db=False) as app:
            app.set_args(["db", "rpc", "get", str(rpc.id)]).run()
            data, output = app.last_rendered
            assert data["out"] == rpc.url


def test_rpc_get_with_rpc_argument(chains: List[ChainFields]) -> None:
    """With RPC argument > it should return the argument"""
    test_rpcs = ["https://www.example-1.com", "https://www.example-2.com"]
    for rpc_url in test_rpcs:
        with Web3CliTest() as app:
            app.set_args(["--rpc", rpc_url, "db", "rpc", "get"]).run()
            data, output = app.last_rendered
            assert data["out"] == rpc_url


def test_rpc_get_with_no_args(chains: List[ChainFields]) -> None:
    """Without arguments > should return an RPC of the user-provided chain"""
    for c in chains:
        with Web3CliTest() as app:
            seed_chains(app, chains)
            app.set_args(["--chain", c["name"], "db", "rpc", "get"]).run()
            data, output = app.last_rendered
            chain: Chain = Chain.select().where(Chain.name == c["name"]).get()
            assert data["out"] in [r.url for r in chain.get_rpcs()]


def test_rpc_delete(chains: List[ChainFields]) -> None:
    with Web3CliTest() as app:
        seed_chains(app, chains)
        rpcs = Rpc.get_all()
    n_rpcs = len(rpcs)
    for i, rpc in enumerate(rpcs):
        with Web3CliTest(delete_db=False) as app:
            app.set_args(
                [
                    "db",
                    "rpc",
                    "delete",
                    str(rpc.id),
                ]
            ).run()
            with pytest.raises(Exception):
                Rpc.get(rpc.id)
            assert Rpc.select().count() == n_rpcs - i - 1
