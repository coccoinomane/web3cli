from tests.main import Web3CliTest
from web3cli.helpers import crypto
import pytest


@pytest.mark.parametrize(
    "msg",
    [
        "d94e4166f0b3c85ffebed3e0eaa7f7680ae296cf8a7229d637472b7452c8602c",
        "3bc2f9b05ac28389fd65fd40068a10f730ec66b6293f9cfd8fe804d212ce06bb",
        "f76c67c2dd62222a5ec747116a66c573f3795c53276c0cdeafbcb5f597e2f8d4",
        "an arbitrary string",
    ],
)
def test_encrypt_decrypt_with_app_key(app_key: bytes, msg: str) -> None:
    with Web3CliTest() as app:
        app.run()
        cypher = crypto.encrypt_string_with_app_key(app, msg)
        decode = crypto.decrypt_string_with_app_key(app, cypher)
        assert msg == decode
