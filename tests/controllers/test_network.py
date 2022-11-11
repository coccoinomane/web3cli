from tests.main import Web3CliTest
from typing import List


def test_network_list() -> None:
    with Web3CliTest() as app:
        app.set_args(["network", "list"]).run()
        data, output = app.last_rendered
        assert "ethereum" in output


def test_network_get(app: Web3CliTest, networks: List[str]) -> None:
    """With explicit argument > return argument value"""
    for network in networks:
        with Web3CliTest() as app:
            app.set_args(["--network", network, "network", "get"]).run()
            data, output = app.last_rendered
            assert data["out"] == network


def test_network_get_no_args(app: Web3CliTest, networks: List[str]) -> None:
    """Without any argument > return the default network"""
    for network in networks:
        with Web3CliTest() as app:
            app.config.set("web3cli", "default_network", network)
            app.set_args(["network", "get"]).run()
            data, output = app.last_rendered
            assert data["out"] == network
