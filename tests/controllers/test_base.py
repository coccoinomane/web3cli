from web3cli.main import Web3CliTest
import web3cli.helpers.args as args


def test_balance(address: str) -> None:
    argv = ["balance", address]
    with Web3CliTest(argv=argv) as app:
        app.run()
        data, output = app.last_rendered
        assert type(data["amount"]) is float
        assert data["amount"] >= 0
        assert data["ticker"] is app.coin
