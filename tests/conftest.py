"""
PyTest Fixtures.
"""

from typing import Any, Iterator, List, Dict
from pytest import FixtureRequest
import pytest
from cement import fs
import secrets
from tests.main import Web3CliTest
from tests.seeder import seed_accounts, seed_local_chain
from web3cli.core.seeds.chain_seeds import chain_seeds
from web3cli.core.seeds.types import ChainSeed
import brownie
from brownie.network.account import Account


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
def chains() -> List[ChainSeed]:
    return chain_seeds


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
    base_app: Web3CliTest, accounts: List[Account], accounts_keys: List[str]
) -> str:
    """An app instance that can be used for tests on the local ganache
    network. It depends on the accounts fixture of brownie, which in
    turn depends on devnetwork fixture, which activates ganache"""
    seed_local_chain(base_app)
    seed_accounts(base_app, accounts, accounts_keys)
    return base_app


@pytest.fixture()
def accounts_keys() -> Iterator[List[str]]:
    """Private keys of the local accounts created by brownie.
    There are just the keys from the mnemonic phrase 'brownie'
    following the standard path m/44'/60'/0'/0/{account_index}"""
    yield [
        "bbfbee4961061d506ffbb11dfea64eba16355cbf1d9c29613126ba7fec0aed5d",
        "804365e293b9fab9bd11bddd39082396d56d30779efbb3ffb0a6089027902c4a",
        "1f52464c2fb44e9b7e0808f2c5fe56d87b73eb3bca0e72c66f9f74d7c6c9a81f",
        "905e216d8acdabbd095f11162327c5e6e80cc59a51283732cd4fe1299b33b7a6",
        "e21bbdc4c57125bec3e05467423dfc3da8754d862140550fc7b3d2833ad1bdeb",
        "b591fb79dd7065964210e7e527c87f97523da07ef8d16794f09750d5eef959b5",
        "fe613f76efbfd03a16624ed8d96777966770f353e83d6f7611c11fdfcdfa48d1",
        "52f94fdeaaf7c8551bda5924f2b52ff438125b9b5170c04ea2e268bd945ff155",
        "a26ebb1df46424945009db72c7a7ba034027450784b93f34000169b35fd3adaa",
        "3ff6c8dfd3ab60a14f2a2d4650387f71fe736b519d990073e650092faaa621fa",
    ]


@pytest.fixture()
def alice() -> Account:
    """A Brownie account preloaded in the local chain"""
    yield brownie.accounts[0]


@pytest.fixture()
def bob() -> Account:
    """A Brownie account preloaded in the local chain"""
    yield brownie.accounts[1]
