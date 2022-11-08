from ..main import Web3CliTest


def test_network_list() -> None:
    argv = ["network", "list"]
    with Web3CliTest(argv=argv) as app:
        app.run()
        data, output = app.last_rendered
        assert "ethereum" in output


def test_network_get(default_network: str) -> None:
    # Without any argument > return the default network
    argv = ["network", "get"]
    with Web3CliTest(argv=argv) as app:
        app.run()
        data, output = app.last_rendered
        assert data["out"] == default_network

    # With explicit argument > return argument value
    argv = ["--network", "binance", "network", "get"]
    with Web3CliTest(argv=argv) as app:
        app.run()
        data, output = app.last_rendered
        assert data["out"] == "binance"
