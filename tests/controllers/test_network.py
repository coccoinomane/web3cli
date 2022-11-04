from web3cli.main import Web3CliTest


def test_network_list() -> None:
    argv = ["network", "list"]
    with Web3CliTest(argv=argv) as app:
        app.run()
        data, output = app.last_rendered
        assert "ethereum" in output


def test_network_get() -> None:
    # Without any argument
    argv = ["network", "get"]
    with Web3CliTest(argv=argv) as app:
        app.run()
        data, output = app.last_rendered
        assert data["out"] is app.config.get("web3cli", "default_network")
    # With explicit argument
    argv = ["--network", "binance", "network", "get"]
    with Web3CliTest(argv=argv) as app:
        app.run()
        data, output = app.last_rendered
        assert data["out"] is "binance"
