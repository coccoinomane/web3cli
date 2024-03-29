"""
PyTest Fixtures.
"""

import json
from pathlib import Path
from typing import Iterator, List

import pytest
from web3.types import ABI

import ape
from tests.ape.tests.helpers.token import deploy_token
from tests.ape.tests.helpers.uniswap import add_v2_liquidity_with_pair, deploy_v2_pair

#   ____   _               _
#  / ___| | |__     __ _  (_)  _ __
# | |     | '_ \   / _` | | | | '_ \
# | |___  | | | | | (_| | | | | | | |
#  \____| |_| |_|  \__,_| |_| |_| |_|


@pytest.fixture(scope="session")
def ape_chain(
    chain: ape.managers.chain.ChainManager,
) -> ape.managers.chain.ChainManager:
    """Alias for the 'chain' fixture of Brownie, to avoid naming
    conflicts with the Chain model of web3core."""
    return chain


@pytest.fixture(scope="session")
def is_eip1559(
    chain: ape.managers.chain.ChainManager,
) -> bool:
    """Return True if the local chain supports eip1599 (type 2 transactions)."""
    return hasattr(chain.blocks[0], "base_fee") or hasattr(
        chain.blocks[0], "base_fee_per_gas"
    )


@pytest.fixture(scope="session")
def ape_chain_name(
    chain: ape.managers.chain.ChainManager,
) -> str:
    """Return whether we are running tests on ganache or anvil."""
    if chain.chain_id == 1337:
        return "ganache"
    elif chain.chain_id == 31337:
        return "anvil"
    raise ValueError(f"Unknown chain type '{chain.chain_id}'")


#     _                                            _
#    / \      ___    ___    ___    _   _   _ __   | |_   ___
#   / _ \    / __|  / __|  / _ \  | | | | | '_ \  | __| / __|
#  / ___ \  | (__  | (__  | (_) | | |_| | | | | | | |_  \__ \
# /_/   \_\  \___|  \___|  \___/   \__,_| |_| |_|  \__| |___/


@pytest.fixture(scope="session")
def alice(accounts: ape.managers.accounts.AccountManager) -> ape.api.AccountAPI:
    """A Brownie account preloaded in the local chain"""
    return accounts[0]


@pytest.fixture(scope="session")
def bob(accounts: ape.managers.accounts.AccountManager) -> ape.api.AccountAPI:
    """A Brownie account preloaded in the local chain"""
    return accounts[1]


@pytest.fixture(scope="session")
def accounts_keys() -> Iterator[List[str]]:
    """Private keys of the local accounts created by ape.
    There are just the keys from the mnemonic phrase
    'test test test test test test test test test test test junk'
    following the standard path m/44'/60'/0'/0/{account_index}"""
    yield [
        "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80",
        "0x59c6995e998f97a5a0044966f0945389dc9e86dae88c7a8412f4603b6b78690d",
        "0x5de4111afa1a4b94908f83103eb1f1706367c2e68ca870fc3fb9a804cdab365a",
        "0x7c852118294e51e653712a81e05800f419141751be58f605c371e15141b007a6",
        "0x47e179ec197488593b187f80a00eb0da91f1b9d0b13f8733639f19c30a34926a",
        "0x8b3a350cf5c34c9194ca85829a2df0ec3153be0318b5e2d3348e872092edffba",
        "0x92db14e403b83dfe3df233f83dfa3a0d7096f21ca9b0d6d6b8d88b2b4ec1564e",
        "0x4bbbf85ce3377467afe5d46f804f221813b2bb87f24d81f60f1fcdbf7cbf4356",
        "0xdbda1821b80551c9d65939329250298aa3472ba22feea921c0cf5d620ea67b97",
        "0x2a871d0798f97d79848a013d4936a73bf4cc922c825d33c1cf7073dff6d409c6",
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


#   ____                   _             _
#  / ___|   ___    _ __   | |_    __ _  (_)  _ __     ___   _ __   ___
# | |      / _ \  | '_ \  | __|  / _` | | | | '_ \   / _ \ | '__| / __|
# | |___  | (_) | | | | | | |_  | (_| | | | | | | | |  __/ | |    \__ \
#  \____|  \___/  |_| |_|  \__|  \__,_| |_| |_| |_|  \___| |_|    |___/


@pytest.fixture(scope="function")
def Token() -> ape.contracts.ContractContainer:
    return ape.project.get_contract("Token")


@pytest.fixture(scope="function")
def UniswapV2Factory() -> ape.contracts.ContractContainer:
    return ape.project.get_contract("UniswapV2Factory")


@pytest.fixture(scope="function")
def UniswapV2Router02() -> ape.contracts.ContractContainer:
    return ape.project.get_contract("UniswapV2Router02")


@pytest.fixture(scope="function")
def UniswapV2Pair() -> ape.contracts.ContractContainer:
    return ape.project.get_contract("UniswapV2Pair")


#  _____           _
# |_   _|   ___   | | __   ___   _ __    ___
#   | |    / _ \  | |/ /  / _ \ | '_ \  / __|
#   | |   | (_) | |   <  |  __/ | | | | \__ \
#   |_|    \___/  |_|\_\  \___| |_| |_| |___/


@pytest.fixture(scope="function")
def WETH(
    accounts: ape.managers.accounts.AccountManager,
    Token: ape.contracts.ContractContainer,
) -> ape.contracts.ContractInstance:
    """A token deployed on the local chain, with 18 decimals, that
    we will use as if it were WETH. Supply of 1 billion tokens, shared between
    all accounts."""
    return deploy_token(
        Token,
        accounts,
        f"WrappedEther",
        f"WETH",
        18,
        10**9,
        True,
    )


@pytest.fixture(scope="function")
def TST(
    accounts: ape.managers.accounts.AccountManager,
    Token: ape.contracts.ContractContainer,
) -> ape.contracts.ContractInstance:
    """TST token deployed on the local chain, with 18 decimals.
    Supply of 1 billion tokens, shared between all accounts."""
    return deploy_token(
        Token,
        accounts,
        f"Test token (18 decimals)",
        f"TST",
        18,
        10**9,
        True,
    )


@pytest.fixture(scope="function")
def TST_0(
    accounts: ape.managers.accounts.AccountManager,
    Token: ape.contracts.ContractContainer,
) -> ape.contracts.ContractInstance:
    """TST_0 token deployed on the local chain, with 18 decimals.
    Supply of 1 billion tokens, shared between all accounts."""
    return deploy_token(
        Token,
        accounts,
        f"Test token 0 (18 decimals)",
        f"TST_0",
        18,
        10**9,
        True,
    )


@pytest.fixture(scope="function")
def TST_1(
    accounts: ape.managers.accounts.AccountManager,
    Token: ape.contracts.ContractContainer,
) -> ape.contracts.ContractInstance:
    """TST_1 token deployed on the local chain, with 18 decimals.
    Supply of 1 billion tokens, shared between all accounts."""
    return deploy_token(
        Token,
        accounts,
        f"Test token 1 (18 decimals)",
        f"TST_1",
        18,
        10**9,
        True,
    )


@pytest.fixture(scope="function")
def TST6(
    accounts: ape.managers.accounts.AccountManager,
    Token: ape.contracts.ContractContainer,
) -> ape.contracts.ContractInstance:
    """TST6 token deployed on the local chain, with 6 decimals.
    Supply of 1 billion tokens, shared between all accounts"""
    return deploy_token(
        Token,
        accounts,
        f"Test token (6 decimals)",
        f"TST6",
        6,
        10**9,
        True,
    )


@pytest.fixture(scope="function")
def TST6_0(
    accounts: ape.managers.accounts.AccountManager,
    Token: ape.contracts.ContractContainer,
) -> ape.contracts.ContractInstance:
    """TST6_0 token deployed on the local chain, with 6
    decimals; each account will have a billion tokens"""
    return deploy_token(
        Token,
        accounts,
        f"Test token 0 (6 decimals)",
        f"TST6_0",
        6,
        10**9,
        True,
    )


@pytest.fixture(scope="function")
def TST6_1(
    accounts: ape.managers.accounts.AccountManager,
    Token: ape.contracts.ContractContainer,
) -> ape.contracts.ContractInstance:
    """TST6_1 token deployed on the local chain, with 6
    decimals; each account will have a billion tokens"""
    return deploy_token(
        Token,
        accounts,
        f"Test token 1 (6 decimals)",
        f"TST6_1",
        6,
        10**9,
        True,
    )


#  _   _           _
# | | | |  _ __   (_)  ___  __      __   __ _   _ __
# | | | | | '_ \  | | / __| \ \ /\ / /  / _` | | '_ \
# | |_| | | | | | | | \__ \  \ V  V /  | (_| | | |_) |
#  \___/  |_| |_| |_| |___/   \_/\_/    \__,_| | .__/
#                                              |_|


@pytest.fixture(scope="function")
def uniswap_v2_factory(
    accounts: ape.managers.accounts.AccountManager,
    UniswapV2Factory: ape.contracts.ContractContainer,
) -> ape.contracts.ContractInstance:
    """The Uniswap factory contract, deployed on the local chain"""
    return UniswapV2Factory.deploy(ape.utils.ZERO_ADDRESS, sender=accounts[0])


@pytest.fixture(scope="function")
def uniswap_v2_router(
    accounts: ape.managers.accounts.AccountManager,
    uniswap_v2_factory: ape.contracts.ContractInstance,
    WETH: ape.contracts.ContractInstance,
    UniswapV2Router02: ape.contracts.ContractContainer,
) -> ape.contracts.ContractInstance:
    """The Uniswap router contract, deployed on the local chain"""
    return UniswapV2Router02.deploy(uniswap_v2_factory, WETH, sender=accounts[0])


@pytest.fixture(scope="function")
def uniswap_v2_pair_WETH_TST(
    accounts: ape.managers.accounts.AccountManager,
    uniswap_v2_factory: ape.contracts.ContractInstance,
    WETH: ape.contracts.ContractInstance,
    TST: ape.contracts.ContractInstance,
    UniswapV2Pair: ape.contracts.ContractContainer,
) -> ape.contracts.ContractInstance:
    """The Uniswap pair contract for tokens WETH-TST, deployed on the
    local chain, with no liquidity."""
    return deploy_v2_pair(accounts[0], (WETH, TST), uniswap_v2_factory, UniswapV2Pair)


@pytest.fixture(scope="function")
def uniswap_v2_pair_TST_0_TST_1(
    accounts: ape.managers.accounts.AccountManager,
    uniswap_v2_factory: ape.contracts.ContractInstance,
    TST_0: ape.contracts.ContractInstance,
    TST_1: ape.contracts.ContractInstance,
    UniswapV2Pair: ape.contracts.ContractContainer,
) -> ape.contracts.ContractInstance:
    """The Uniswap pair contract for tokens TST_0-TST_1, deployed on the
    local chain, with no liquidity."""
    return deploy_v2_pair(
        accounts[0], (TST_0, TST_1), uniswap_v2_factory, UniswapV2Pair
    )


@pytest.fixture(scope="function")
def uniswap_v2_pair_TST_0_TST_1_with_liquidity(
    accounts: ape.managers.accounts.AccountManager,
    TST_0: ape.contracts.ContractInstance,
    TST_1: ape.contracts.ContractInstance,
    uniswap_v2_pair_TST_0_TST_1: ape.contracts.ContractInstance,
    uniswap_v2_factory: ape.contracts.ContractInstance,
    UniswapV2Pair: ape.contracts.ContractContainer,
) -> ape.contracts.ContractInstance:
    """The Uniswap pair contract for tokens TST_0-TST_1, deployed on the
    local chain, with 1 TST_0 and 1 TST_1 of reserves."""
    add_v2_liquidity_with_pair(
        accounts[0],
        (TST_0, TST_1),
        (10**18, 10**18),
        uniswap_v2_factory,
        UniswapV2Pair,
    )
    return uniswap_v2_pair_TST_0_TST_1
