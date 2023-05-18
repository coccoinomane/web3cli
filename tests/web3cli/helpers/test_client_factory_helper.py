from typing import List

import pytest

from tests.web3cli.main import Web3CliTest
from web3cli.helpers.client_factory import make_client
from web3core.helpers.seed import seed_chains
from web3core.models.types import ChainFields


@pytest.mark.remote
def test_make_client(chains: List[ChainFields]) -> None:
    for chain in chains:
        with Web3CliTest() as app:
            seed_chains(chains)
            app.set_args(argv=["--chain", chain["name"], "version"]).run()
            client = make_client(app)
            block = client.get_latest_block()
            assert type(block.get("number")) is int
            assert block.get("number") >= 0
            assert type(block.get("size")) is int
            assert block.get("size") >= 0
            assert type(block.get("difficulty")) is int
            assert block.get("difficulty") >= 0
            assert type(block.get("transactions")) is list
