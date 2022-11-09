from web3cli.core.helpers import crypto
import secrets
import pytest


@pytest.mark.parametrize(
    "msg",
    [
        b"d94e4166f0b3c85ffebed3e0eaa7f7680ae296cf8a7229d637472b7452c8602c",
        b"3bc2f9b05ac28389fd65fd40068a10f730ec66b6293f9cfd8fe804d212ce06bb",
        b"f76c67c2dd62222a5ec747116a66c573f3795c53276c0cdeafbcb5f597e2f8d4",
        b"an arbitrary binary",
    ],
)
def test_encrypt_decrypt(msg: bytes) -> None:
    key = secrets.token_bytes(32)
    assert msg == crypto.decrypt(crypto.encrypt(msg, key), key)
