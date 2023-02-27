"""
PyTest Fixtures.
"""

import json
from pathlib import Path
from typing import Any, Iterator, List

import pytest
from web3.types import ABI

from brownie.network import Chain as BrownieChain
from brownie.network.account import Account as BrownieAccount
from brownie.network.contract import Contract as BrownieContract
from brownie.network.contract import ContractContainer as BrownieContractContainer
from tests.brownie.tests.helper import deploy_token

#   ____   _               _
#  / ___| | |__     __ _  (_)  _ __
# | |     | '_ \   / _` | | | | '_ \
# | |___  | | | | | (_| | | | | | | |
#  \____| |_| |_|  \__,_| |_| |_| |_|


@pytest.fixture(scope="session")
def ganache(chain: BrownieChain) -> BrownieChain:
    """Alias for the 'chain' fixture of Brownie, to avoid naming
    conflicts with the Chain model of web3core."""
    return chain


@pytest.fixture(scope="function", autouse=True)
def isolate(fn_isolation: Any) -> None:
    """Reset the local blockchain before each single test.
    https://eth-brownie.readthedocs.io/en/stable/tests-pytest-intro.html"""
    pass


#     _                                            _
#    / \      ___    ___    ___    _   _   _ __   | |_   ___
#   / _ \    / __|  / __|  / _ \  | | | | | '_ \  | __| / __|
#  / ___ \  | (__  | (__  | (_) | | |_| | | | | | | |_  \__ \
# /_/   \_\  \___|  \___|  \___/   \__,_| |_| |_|  \__| |___/


@pytest.fixture(scope="session")
def alice(accounts: List[BrownieAccount]) -> BrownieAccount:
    """A Brownie account preloaded in the local chain"""
    yield accounts[0]


@pytest.fixture(scope="session")
def bob(accounts: List[BrownieAccount]) -> BrownieAccount:
    """A Brownie account preloaded in the local chain"""
    yield accounts[1]


@pytest.fixture(scope="session")
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


#     _      ____    ___
#    / \    | __ )  |_ _|
#   / _ \   |  _ \   | |
#  / ___ \  | |_) |  | |
# /_/   \_\ |____/  |___|


@pytest.fixture(scope="session")
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


@pytest.fixture(scope="session")
def erc20_abi_string() -> Iterator[str]:
    """The ABI for the ERC20 token standard, as a string"""
    yield '[{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_spender","type":"address"},{"name":"_value","type":"uint256"}],"name":"approve","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transferFrom","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"},{"name":"_spender","type":"address"}],"name":"allowance","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"payable":true,"stateMutability":"payable","type":"fallback"},{"anonymous":false,"inputs":[{"indexed":true,"name":"owner","type":"address"},{"indexed":true,"name":"spender","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"from","type":"address"},{"indexed":true,"name":"to","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Transfer","type":"event"}]'


@pytest.fixture(scope="function")
def erc20_abi_file(tmp_path: Path, erc20_abi_string: str) -> Iterator[str]:
    """The path of a JSON file containing the ABI for the ERC20 token
    standard"""
    f = tmp_path / "erc20.json"
    f.write_text(erc20_abi_string)
    yield str(f)


@pytest.fixture(scope="session")
def erc20_abi(erc20_abi_string: str) -> Iterator[ABI]:
    """The ABI for the ERC20 token standard, as a JSON object"""
    yield json.loads(erc20_abi_string)


#  _____           _
# |_   _|   ___   | | __   ___   _ __    ___
#   | |    / _ \  | |/ /  / _ \ | '_ \  / __|
#   | |   | (_) | |   <  |  __/ | | | | \__ \
#   |_|    \___/  |_|\_\  \___| |_| |_| |___/


@pytest.fixture(scope="module")
def weth(
    Token: BrownieContractContainer, accounts: List[BrownieAccount]
) -> BrownieContract:
    """A token deployed on the local chain, with 18 decimals, that
    we will use as if it were WETH; each account will have 1000."""
    return deploy_token(
        Token,
        accounts,
        f"Wrapper Ether",
        f"WETH",
        18,
        10000,
        True,
    )


@pytest.fixture(scope="module")
def token(
    Token: BrownieContractContainer, accounts: List[BrownieAccount]
) -> BrownieContract:
    """The TST_0 token deployed on the local chain, with 18 decimals;
    each account will have 1000 of each token"""
    return deploy_token(
        Token,
        accounts,
        f"Test token (18 decimals)",
        f"TST",
        18,
        10000,
        True,
    )


@pytest.fixture(scope="module")
def token_pair(
    Token: BrownieContractContainer,
    accounts: List[BrownieAccount],
) -> List[BrownieContract]:
    """Tokens TST_0 and TST_1, deployed on the local chain, with 18 decimals;
    each account will have 1000 of each token"""
    return [
        deploy_token(
            Token,
            accounts,
            f"Test token {i} (18 decimals)",
            f"TST_{i}",
            18,
            10000,
            True,
        )
        for i in range(len(accounts))
    ]


@pytest.fixture(scope="module")
def token6(
    Token: BrownieContractContainer, accounts: List[BrownieAccount]
) -> BrownieContract:
    """The TST6_0 token deployed on the local chain, with 6 decimals;
    each account will have 1000 of each token"""
    return deploy_token(
        Token,
        accounts,
        f"Test token (6 decimals)",
        f"TST",
        6,
        10000,
        True,
    )


@pytest.fixture(scope="module")
def token6_pair(
    Token: BrownieContractContainer,
    accounts: List[BrownieAccount],
) -> List[BrownieContract]:
    """Tokens TST6_0 and TST6_1, deployed on the local chain, with 6 decimals;
    each account will have 1000 of each token"""
    return [
        deploy_token(
            Token,
            accounts,
            f"Test token {i} (6 decimals)",
            f"TST6_{i}",
            6,
            10000,
            True,
        )
        for i in range(len(accounts))
    ]


#  _   _           _
# | | | |  _ __   (_)  ___  __      __   __ _   _ __
# | | | | | '_ \  | | / __| \ \ /\ / /  / _` | | '_ \
# | |_| | | | | | | | \__ \  \ V  V /  | (_| | | |_) |
#  \___/  |_| |_| |_| |___/   \_/\_/    \__,_| | .__/
#                                              |_|


@pytest.fixture(scope="module")
def uniswap_v2_factory(
    accounts: List[BrownieAccount],
    UniswapV2Factory: BrownieContractContainer,
) -> BrownieContract:
    """The Uniswap factory contract, deployed on the local chain"""
    return UniswapV2Factory.deploy(accounts[0], {"from": accounts[0]})


@pytest.fixture(scope="module")
def uniswap_v2_router(
    accounts: List[BrownieAccount],
    UniswapV2Router02: BrownieContractContainer,
    uniswap_v2_factory: BrownieContract,
    weth: BrownieContract,
) -> BrownieContract:
    """The Uniswap router contract, deployed on the local chain"""
    return UniswapV2Router02.deploy(
        uniswap_v2_factory.address, weth.address, {"from": accounts[0]}
    )


@pytest.fixture(scope="module")
def uniswap_v2_pair_weth_tst(
    accounts: List[BrownieAccount],
    uniswap_v2_factory: BrownieContract,
    weth: BrownieContract,
    token: BrownieContract,
    UniswapV2Pair: BrownieContractContainer,
) -> BrownieContract:
    """The Uniswap pair contract for WETH-TST, deployed on the
    local chain"""
    uniswap_v2_factory.createPair(weth.address, token.address, {"from": accounts[0]})
    address = uniswap_v2_factory.getPair(weth.address, token.address)
    return UniswapV2Pair.at(address)