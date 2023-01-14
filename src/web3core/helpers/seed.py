from typing import Any, Dict, List

from web3core.models.address import Address
from web3core.models.chain import Chain
from web3core.models.contract import Contract, ContractType
from web3core.models.signer import Signer
from web3core.models.tx import Tx
from web3core.models.types import (
    AddressFields,
    ChainFields,
    ContractFields,
    ContractTypeFields,
    TxFields,
)
from web3core.seeds import chain_seeds, contract_seeds, contract_type_seeds


def populate_db() -> None:
    """Fill the database with a few common-sense values: popular chains,
    known address tags, trusted contracts and tokens, etc"""
    seed_chains(chain_seeds.all)
    seed_contracts(contract_seeds.all)


def seed_chain(chain: ChainFields) -> Chain:
    """Add the given chain to the database"""
    return Chain.seed_one(chain)


def seed_chains(chains: List[ChainFields]) -> List[Chain]:
    """Add the given chains to the database"""
    return Chain.seed(chains)


def seed_contract(contract: ContractFields) -> Contract:
    """Add the given contract to the database"""
    seed_contract_types(contract_type_seeds.all)
    return Contract.upsert(contract)


def seed_contracts(contracts: List[ContractFields]) -> List[Contract]:
    """Add the given contracts to the database"""
    seed_contract_types(contract_type_seeds.all)
    return [Contract.upsert(c) for c in contracts]


def seed_contract_types(contract_types: List[ContractTypeFields]) -> List[ContractType]:
    """Add the given contract types to the database"""
    return [ContractType.upsert(ct) for ct in contract_types]


def seed_addresses(addresses: List[AddressFields]) -> List[Address]:
    """Add the given addresses to the database"""
    return [Address.upsert(a) for a in addresses]


def seed_signers(signers: List[Dict[str, Any]], password: bytes) -> List[Signer]:
    """Add the given signers to the database"""
    return [
        Signer.create_encrypt(name=s["name"], key=s["private_key"], pwd=password)
        for s in signers
    ]


def seed_txs(txs: List[TxFields]) -> List[Tx]:
    """Add the given transactions to the database"""
    return [Tx.upsert(t) for t in txs]
