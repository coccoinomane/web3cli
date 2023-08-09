"""
PyTest Fixtures.
"""

from typing import Any, Dict, Iterator, List

import pytest
from playhouse.sqlite_ext import SqliteExtDatabase

from web3core.db import DB
from web3core.helpers.database import init_db
from web3core.models import MODELS
from web3core.models.chain import Chain
from web3core.models.types import AddressFields, ChainFields, ContractFields, TxFields
from web3core.seeds import chain_seeds, contract_seeds


@pytest.fixture(scope="function")
def db() -> Iterator[SqliteExtDatabase]:
    init_db(DB, MODELS, ":memory:")
    yield DB
    DB.drop_tables(MODELS)
    DB.close()


@pytest.fixture(scope="session")
def addresses() -> List[AddressFields]:
    return [
        {
            "name": "Ethereum foundation",
            "address": "0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae",
            "desc": "Test wallet EF",
        },
        {
            "name": "Binance hot wallet",
            "address": "0x8894e0a0c962cb723c1976a4421c95949be2d4e3",
            "desc": "Test wallet BHW",
        },
        {
            "name": "Alameda research",
            "address": "0xbefe4f86f189c1c817446b71eb6ac90e3cb68e60",
            "desc": "Test wallet AR",
        },
    ]


@pytest.fixture(scope="session")
def signers() -> List[Dict[str, Any]]:
    return [
        {
            "name": "vanity_1",
            "address": "0x0c2010dc4736bab060740D3968cf1dDF86196D81",
            "private_key": "d94e4166f0b3c85ffebed3e0eaa7f7680ae296cf8a7229d637472b7452c8602c",
            "keyfile": '{"address": "0c2010dc4736bab060740d3968cf1ddf86196d81", "crypto": {"cipher": "aes-128-ctr", "cipherparams": {"iv": "44bb6afb52fa1eb4e273f2dc972aa9c9"}, "ciphertext": "ca4bd4f91bfc51a34e5fd72340cfe058ae77108c51fdad8413c1a7c1eb54ea5c", "kdf": "scrypt", "kdfparams": {"dklen": 32, "n": 262144, "r": 1, "p": 8, "salt": "34eb69126e4c28c3b96ff2bbafc30fd6"}, "mac": "e30f84c256b85ad757527a9963da856a3dc0c8ff7691eaa30dce8a6025db0044"}, "id": "5dcac562-ed62-42be-85af-458082ae5621", "version": 3}',
            "keyfile_password": "secret_1",
        },
        {
            "name": "vanity_2",
            "address": "0x206D4d644c22dDFc343b3AD23bBc7A42c8B201fc",
            "private_key": "3bc2f9b05ac28389fd65fd40068a10f730ec66b6293f9cfd8fe804d212ce06bb",
            "keyfile": '{"address": "206d4d644c22ddfc343b3ad23bbc7a42c8b201fc", "crypto": {"cipher": "aes-128-ctr", "cipherparams": {"iv": "8eb93057b97baef092028a49d729fadb"}, "ciphertext": "5bcb8cc45abc29098e6157953218f90ce992c410fefa5cd6ccba5f90301abbfc", "kdf": "scrypt", "kdfparams": {"dklen": 32, "n": 262144, "r": 1, "p": 8, "salt": "9a9bae4fbef319b359dbc1a19757898c"}, "mac": "a890fbe5e0472cecff264b50ed7be3d56c22082a45e836712604a117ccc2ea24"}, "id": "c77dd2d2-d657-4d4a-ab7c-b491c4be0eb9", "version": 3}',
            "keyfile_password": "secret_2",
        },
        {
            "name": "vanity_3",
            "address": "0x9fF0c40eDe4585a5E9f0F00009ce79b6344cB663",
            "private_key": "f76c67c2dd62222a5ec747116a66c573f3795c53276c0cdeafbcb5f597e2f8d4",
            "keyfile": '{"address": "9ff0c40ede4585a5e9f0f00009ce79b6344cb663", "crypto": {"cipher": "aes-128-ctr", "cipherparams": {"iv": "efddd96d2ce2f840af8b58d681d1330c"}, "ciphertext": "95d4fc9dde914a8cdb679fda7b0ead7312fcc3053bfeb82bd5f6ffa5db22da4b", "kdf": "scrypt", "kdfparams": {"dklen": 32, "n": 262144, "r": 1, "p": 8, "salt": "1dc311b9bd5c76ed686ef39003716294"}, "mac": "63cdddd9e8f3987dff63a88ef838cc24ecfeb7b568916f581deb061844850f5e"}, "id": "c78bb6ff-fb12-474a-bf84-5a6d6e8e8bcc", "version": 3}',
            "keyfile_password": "secret_3",
        },
    ]


@pytest.fixture(scope="session")
def txs() -> List[TxFields]:
    return [
        {
            "hash": "0xbe62871b8c0545dd9034bcb8e802b0c024d2983ba1de663c5cbb1b02c9173609",
            "chain": "eth",
            "to": "0xd2b06119B51626F175375C8Fb5Baa0c0e54819f2",
            "from_": "0xFdEE07396b59aEE88555bfb6C683Ca8FF3Ffd35c",
            "value": "9461431800000000000",
            "gas": 21000,
            "gas_price": "19000000000",
            "desc": "A regular value transaction",
            "data": "",
            "receipt": "",
            "created_at": "2022-12-02 19:45:57.100147+01:00",
            "updated_at": "2022-12-02 19:45:57.100172+01:00",
        },
        {
            "hash": "0xdf92dbca5a2788c4c57ee76408d1ea35c3753b6ababb468a1d949af56e786338",
            "chain": "eth",
            "to": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
            "from_": "0x13E464A06df694893f6B07E49b6d84D4bece04c9",
            "value": None,
            "gas": 63209,
            "gas_price": "12250771391",
            "desc": "An ERC-20 transfer (USDT)",
            "data": "0xa9059cbb0000000000000000000000002fe5dbe5b4cdf1a032ab230f258d129b38faf79f00000000000000000000000000000000000000000000000000000009f7142c00",
            "receipt": "",
            "created_at": "2021-12-01 19:45:57.100147+01:00",
            "updated_at": "2021-12-01 19:45:57.100172+01:00",
        },
    ]


@pytest.fixture(scope="session")
def chains() -> List[ChainFields]:
    """Chains to seed the test DB with.  Keep the
    number of chains low lest we slow down tests."""
    return [chain_seeds.eth, chain_seeds.bnb, chain_seeds.era]


@pytest.fixture(scope="session")
def contracts(chains: List[Chain]) -> List[ContractFields]:
    """List of contracts to seed the test DB with.  Keep the
    number of contracts low lest we slow down tests."""
    contracts = []
    for chain in chains:
        chain_contracts = [
            contract
            for contract in contract_seeds.all
            if chain["name"] == contract["chain"]
        ]
        contracts += chain_contracts[:3]
    return contracts


@pytest.fixture(scope="session")
def contract_without_abi(contracts: List[ContractFields]) -> ContractFields:
    contracts[0]["abi"] = None
    return contracts[0]
