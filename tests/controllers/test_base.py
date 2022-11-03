from web3cli.main import Web3CliTest
import web3cli.helpers.args as args


def test_network_arg() -> None:
    # Without any argument
    argv = ["network", "get"]
    with Web3CliTest(argv=argv) as app:
        app.run()
        assert app.network is app.config.get("web3cli", "default_network")
    # With explicit argument
    argv = ["--network", "binance", "network", "get"]
    with Web3CliTest(argv=argv) as app:
        app.run()
        assert app.network is "binance"


def test_balance(address: str) -> None:
    argv = ["balance", address]
    with Web3CliTest(argv=argv) as app:
        app.run()
        data, output = app.last_rendered
        assert type(data["amount"]) is float
        assert data["amount"] >= 0
        assert data["ticker"] is app.coin
