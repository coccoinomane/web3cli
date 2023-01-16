"""
PyTest Fixtures.
"""

import secrets
from typing import Iterator, List

import pytest

from brownie.network.account import Account as BrownieAccount
from tests.seed import seed_local_accounts, seed_local_chain
from tests.web3cli.main import Web3CliTest


@pytest.fixture()
def app_key() -> bytes:
    """A randomly-generated key suitable to be used as application key"""
    return secrets.token_bytes(32)


@pytest.fixture()
def base_app(app_key: bytes) -> Iterator[Web3CliTest]:
    """An app instance that can be used for basic tests. Add
    arguments with app.set_argv() and run the CLI with app.run()"""
    app = Web3CliTest()
    app.setup()
    app.config.set("web3cli", "app_key", app_key)
    yield app
    app.close()


@pytest.fixture()
def app(
    base_app: Web3CliTest, accounts: List[BrownieAccount], accounts_keys: List[str]
) -> Iterator[Web3CliTest]:
    """An app instance that can be used for tests on the local ganache
    network.

    It has Brownie's accounts preloaded as signers.

    It depends on the accounts fixture of brownie, which in
    turn depends on devnetwork fixture, which activates ganache"""
    seed_local_chain(base_app)
    seed_local_accounts(base_app, accounts, accounts_keys)
    yield base_app
