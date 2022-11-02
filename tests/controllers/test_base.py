from web3cli.main import Web3CliTest
import web3cli.core.args as args


def test_network_arg() -> None:
    # Without any argument
    argv = ["network", "get"]
    with Web3CliTest(argv=argv) as app:
        app.run()
        assert args.get_network(app) is app.config.get("web3cli", "default_network")
    # With explicit argument
    argv = ["--network", "binance", "network", "get"]
    with Web3CliTest(argv=argv) as app:
        app.run()
        assert args.get_network(app) is "binance"
