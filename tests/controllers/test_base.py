from typing import Any, Dict, List
from tests.main import Web3CliTest
import pytest
from tests.seeder import seed_signers
import ast


@pytest.mark.slow
def test_balance() -> None:
    with Web3CliTest() as app:
        app.set_args(["balance", "0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae"]).run()
        data, output = app.last_rendered
        assert type(data["amount"]) is float
        assert data["amount"] >= 0
        assert data["ticker"] is app.coin


@pytest.mark.parametrize(
    "msg",
    [
        "Hello world!",
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam pulvinar lacus erat, et sollicitudin purus rutrum sed. Aliquam pulvinar nunc nec sagittis sagittis. Nunc efficitur lacus urna, sed dapibus lacus varius id. Nam laoreet convallis nisl, ut lacinia sem congue eu. Phasellus eu nisi in lectus lobortis viverra a at diam. Nulla dolor nisl, mollis efficitur venenatis in, elementum consequat quam. Sed a euismod justo, quis maximus velit. Maecenas varius augue dolor, sit amet elementum lacus pretium vitae. Fusce egestas condimentum quam eget elementum. Suspendisse vulputate ut urna a pretium. Nunc semper a sem fermentum dapibus.",
        "I will copiously donate to coccoinomane ❤️",
    ],
)
def test_sign(msg: str, signers: List[Dict[str, Any]]) -> None:
    with Web3CliTest() as app:
        seed_signers(app, [signers[0]])
        app.set_args(["sign", msg]).run()
        data, output = app.last_rendered
        assert "messageHash" in data["out"]
        assert "r" in data["out"]
        assert "s" in data["out"]
        assert "v" in data["out"]
        assert "signature" in data["out"]
