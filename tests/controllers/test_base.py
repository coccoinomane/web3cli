from ..main import Web3CliTest
import pytest


@pytest.mark.slow
def test_balance() -> None:
    with Web3CliTest() as app:
        app.set_args(["balance", "0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae"]).run()
        data, output = app.last_rendered
        assert type(data["amount"]) is float
        assert data["amount"] >= 0
        assert data["ticker"] is app.coin
