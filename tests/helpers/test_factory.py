from typing import List
from tests.main import Web3CliTest
from web3cli.helpers.args import parse_global_args
from web3cli.helpers.factory import make_client
from web3client.helpers.debug import pprintAttributeDict


def test_make_client(networks: List[str]) -> None:
    for network in networks:
        argv = ["--network", network, "version"]  # simplest possible command
        with Web3CliTest(argv=argv) as app:
            app.run()
            client = make_client(app)
            block = client.getLatestBlock()
            assert type(block.get("number")) is int
            assert block.get("number") >= 0
            assert type(block.get("size")) is int
            assert block.get("size") >= 0
            assert type(block.get("difficulty")) is int
            assert block.get("difficulty") >= 0
            assert type(block.get("transactions")) is list
