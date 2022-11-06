from web3cli.main import Web3CliTest


def test_balance() -> None:
    argv = ["balance", "0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae"]
    with Web3CliTest(argv=argv) as app:
        app.run()
        data, output = app.last_rendered
        assert type(data["amount"]) is float
        assert data["amount"] >= 0
        assert data["ticker"] is app.coin
