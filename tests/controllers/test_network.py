from ..main import Web3CliTest
from typing import List


def test_network_list() -> None:
    argv = ["network", "list"]
    with Web3CliTest(argv=argv) as app:
        app.run()
        data, output = app.last_rendered
        assert "ethereum" in output


def test_network_get(networks: List[str]) -> None:
    # Without any argument > return the default network
    for network in networks:
        argv = ["network", "get"]
        with Web3CliTest(argv=argv) as app:
            app.config.set("web3cli", "default_network", network)
            app.run()
            data, output = app.last_rendered
            assert data["out"] == network

    # With explicit argument > return argument value
    for network in networks:
        argv = ["--network", network, "network", "get"]
        with Web3CliTest(argv=argv) as app:
            app.run()
            data, output = app.last_rendered
            assert data["out"] == network
