from typing import Any, Dict, List
from tests.main import Web3CliTest
from tests.seeder import seed_signers
from web3cli.helpers.client_factory import make_client, make_wallet
import pytest


@pytest.mark.slow
def test_make_client(chains: List[str]) -> None:
    for chain in chains:
        argv = ["--chain", chain, "version"]  # simplest possible command
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


@pytest.mark.slow
def test_make_wallet(
    chains: List[str], signers: List[Dict[str, Any]], app_key: bytes
) -> None:
    """Sign a message with a wallet created by make_wallet"""
    msg = "Hello world"
    s = signers[0]
    for chain in chains:
        argv = [
            "--chain",
            chain,
            "--signer",
            s["label"],
            "version",  # simplest possible command
        ]
        with Web3CliTest(argv=argv) as app:
            seed_signers(app, [s])
            app.run()
            client = make_wallet(app)
            signed_message = client.signMessage(msg)
            assert client.isMessageSignedByMe(msg, signed_message) == True
