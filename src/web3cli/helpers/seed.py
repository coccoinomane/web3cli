from typing import Any, Dict, List

from cement import App

from web3cli.helpers.database import db_ready_or_raise
from web3core.models.address import Address
from web3core.models.chain import Chain
from web3core.models.contract import Contract
from web3core.models.signer import Signer
from web3core.models.tx import Tx
from web3core.models.types import AddressFields, ChainFields, ContractFields, TxFields
from web3core.seeds import chain_seeds, contract_seeds


def populate_db(app: App) -> None:
    """Fill the database with a few common-sense values: popular chains,
    known address tags, trusted contracts and tokens, etc"""
    db_ready_or_raise(app)
    app.log.debug("Seeding database...")
    seed_chains(app, chain_seeds.all)
    seed_contracts(app, contract_seeds.all)


def seed_chain(app: App, chain: ChainFields, make_default: bool = True) -> Chain:
    """Add the given chain to the database, and optionally
    make it the default network"""
    db_ready_or_raise(app)
    if make_default:
        app.config.set("web3cli", "default_chain", chain["name"])
    return Chain.seed_one(chain)


def seed_chains(app: App, chains: List[ChainFields]) -> List[Chain]:
    """Add the given chains to the database"""
    db_ready_or_raise(app)
    return Chain.seed(chains)


def seed_contracts(app: App, contracts: List[ContractFields]) -> List[Contract]:
    """Add the given contracts to the database"""
    db_ready_or_raise(app)
    return [Contract.upsert(c) for c in contracts]


def seed_addresses(app: App, addresses: List[AddressFields]) -> List[Address]:
    """Add the given addresses to the database"""
    db_ready_or_raise(app)
    return [Address.upsert(a) for a in addresses]


def seed_signers(app: App, signers: List[Dict[str, Any]]) -> List[Signer]:
    """Add the given signers to the database"""
    db_ready_or_raise(app)
    return [
        Signer.create_encrypt(name=s["name"], key=s["private_key"], pwd=app.app_key)
        for s in signers
    ]


def seed_txs(app: App, txs: List[TxFields]) -> List[Tx]:
    """Add the given transactions to the database"""
    db_ready_or_raise(app)
    return [Tx.upsert(t) for t in txs]
