from tests.main import Web3CliTest
from typing import List
from tests.seeder import seed_chains
from web3cli.core.exceptions import RpcIsInvalid, Web3CliError
from web3cli.core.models.chain import Chain
from web3cli.core.seeds.types import ChainSeed
import pytest
from web3cli.core.helpers.format import cut


def test_rpc_list(chains: List[ChainSeed]) -> None:
    with Web3CliTest() as app:
        seed_chains(app, chains)
        app.set_args(["rpc", "list"]).run()
        data, output = app.last_rendered
        for c in chains:
            for rpc_url in c["rpcs"]:
                assert (
                    rpc_url[0 : app.config.get("web3cli", "output_table_wrap")]
                    in output
                )


def test_rpc_add(chains: List[ChainSeed]) -> None:
    c = chains[0]
    # Add two different RPCs > they should be in the DB
    test_rpcs = ["https://www.example-1.com", "https://www.example-2.com"]
    with Web3CliTest() as app:
        chain = Chain.create(name=c["name"], chain_id=c["chain_id"], coin=c["coin"])
        app.set_args(["rpc", "add", chain.name] + test_rpcs).run()
        created_rpcs = chain.get_rpcs()
        assert len(created_rpcs) == len(test_rpcs)
        for i, rpc in enumerate(created_rpcs):
            assert rpc.url == test_rpcs[i]
    # Add the same RPCs again > they should not be added to the db
    with Web3CliTest(delete_db=False) as app:
        app.set_args(["rpc", "add", chain.name] + test_rpcs).run()
        assert len(chain.get_rpcs()) == len(test_rpcs)
    # Add an RPC with a wrong URL > it should raise
    with Web3CliTest() as app:
        chain = Chain.create(name=c["name"], chain_id=c["chain_id"], coin=c["coin"])
        with pytest.raises(RpcIsInvalid):
            app.set_args(["rpc", "add", chain.name, "not a URI"]).run()
