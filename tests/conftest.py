"""
PyTest Fixtures.
"""

from typing import Any, List, Dict
from pytest import FixtureRequest
import pytest
from cement import fs
import secrets
from tests.main import Web3CliTest
from web3cli.main import Web3Cli


@pytest.fixture()
def addresses() -> List[Dict[str, Any]]:
    return [
        {
            "label": "Ethereum foundation",
            "address": "0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae",
            "description": "Test wallet EF",
        },
        {
            "label": "Binance hot wallet",
            "address": "0x8894e0a0c962cb723c1976a4421c95949be2d4e3",
            "description": "Test wallet BHW",
        },
        {
            "label": "Alameda research",
            "address": "0xbefe4f86f189c1c817446b71eb6ac90e3cb68e60",
            "description": "Test wallet AR",
        },
    ]


@pytest.fixture()
def signers() -> List[Dict[str, Any]]:
    return [
        {
            "label": "vanity_1",
            "address": "0x0c2010dc4736bab060740D3968cf1dDF86196D81",
            "private_key": "d94e4166f0b3c85ffebed3e0eaa7f7680ae296cf8a7229d637472b7452c8602c",
        },
        {
            "label": "vanity_2",
            "address": "0x206D4d644c22dDFc343b3AD23bBc7A42c8B201fc",
            "private_key": "3bc2f9b05ac28389fd65fd40068a10f730ec66b6293f9cfd8fe804d212ce06bb",
        },
        {
            "label": "vanity_3",
            "address": "0x9fF0c40eDe4585a5E9f0F00009ce79b6344cB663",
            "private_key": "f76c67c2dd62222a5ec747116a66c573f3795c53276c0cdeafbcb5f597e2f8d4",
        },
    ]


@pytest.fixture()
def chains() -> List[str]:
    return ["ethereum", "binance", "avalanche", "swimmer"]


@pytest.fixture()
def app_key() -> bytes:
    """A randomly-generated key suitable to be used as application key"""
    return secrets.token_bytes(32)


@pytest.fixture(scope="function")
def tmp(request: FixtureRequest) -> Any:
    """Create a `tmp` object that geneates a unique temporary directory, and
    file for each test function that requires it."""
    t = fs.Tmp()
    yield t
    t.remove()


@pytest.fixture()
def app(app_key: bytes) -> Any:
    """A CLI instance that can be used for tests. Add arguments as a list
    of strings with app.set_argv(), and run the CLI with app.run()"""
    app = Web3CliTest()
    app.setup()
    app.config.set("web3cli", "app_key", app_key)
    yield app
    app.close()
