from ..main import Web3CliTest
import ast


def test_key_create() -> None:
    argv = [
        "key",
        "create",
    ]
    with Web3CliTest(argv=argv) as app:
        print(app.config.get("web3cli", "app_key"))
        assert not app.config.get("web3cli", "app_key")
        app.run()
        key: str = app.config.get("web3cli", "app_key")
        assert key.startswith("b'.")
