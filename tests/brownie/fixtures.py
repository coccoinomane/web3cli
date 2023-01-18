"""
PyTest Fixtures.
"""

import json
from typing import Iterator, List

import pytest
from brownie_tokens import ERC20
from web3.types import ABI

from brownie.network.account import Account as BrownieAccount
from brownie.network.contract import Contract as BrownieContract


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
def simple_abi() -> Iterator[ABI]:
    """A simple ABI for a contract with a single function"""
    yield [
        {
            "constant": False,
            "inputs": [{"name": "a", "type": "uint256"}],
            "name": "foo",
            "outputs": [],
            "payable": False,
            "stateMutability": "nonpayable",
            "type": "function",
        }
    ]


@pytest.fixture()
def erc20_abi() -> Iterator[ABI]:
    """The ABI for the ERC20 token standard"""
    yield json.loads(
        '[{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_spender","type":"address"},{"name":"_value","type":"uint256"}],"name":"approve","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transferFrom","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"},{"name":"_spender","type":"address"}],"name":"allowance","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"payable":true,"stateMutability":"payable","type":"fallback"},{"anonymous":false,"inputs":[{"indexed":true,"name":"owner","type":"address"},{"indexed":true,"name":"spender","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"from","type":"address"},{"indexed":true,"name":"to","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Transfer","type":"event"}]'
    )


@pytest.fixture()
def alice(accounts: List[BrownieAccount]) -> BrownieAccount:
    """A Brownie account preloaded in the local chain"""
    yield accounts[0]


@pytest.fixture()
def bob(accounts: List[BrownieAccount]) -> BrownieAccount:
    """A Brownie account preloaded in the local chain"""
    yield accounts[1]


@pytest.fixture(scope="session")
def token18(accounts: List[BrownieAccount]) -> BrownieContract:
    """The TST18 token deployed on the local chain, with
    18 decimals; each account will have 100 tokens"""
    token = ERC20(name="Test Token", symbol="TST18", decimals=18)
    for account in accounts:
        token._mint_for_testing(account.address, 100 * 10**18)
    yield token


@pytest.fixture(scope="session")
def token6(accounts: List[BrownieAccount]) -> BrownieContract:
    """The TST6 token deployed on the local chain, with
    6 decimals; each account will have 100 tokens"""
    token = ERC20(name="Test Token", symbol="TST", decimals=6)
    for account in accounts:
        token._mint_for_testing(account.address, 100 * 10**6)
    yield token
