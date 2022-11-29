"""Please note this file DOES NOT contain tests, but
helper functions to better run tests"""

from typing import Any, Dict, List
from web3cli.core.exceptions import Web3CliError
from web3cli.core.models.chain import Chain
from web3cli.core.seeds.types import ChainSeed
from web3cli.core.seeds.chain_seeds import local_chain
from web3cli.helpers.database import db_ready_or_raise
from web3cli.main import Web3Cli
from web3cli.core.models.address import Address
from web3cli.core.models.signer import Signer
from brownie.network.account import Account
import brownie


def seed_chain(app: Web3Cli, chain: ChainSeed, make_default: bool = True) -> Chain:
    """Add the given seed chain to the database, and optionally
    make it the default network"""
    db_ready_or_raise(app)
    if make_default:
        app.config.set("web3cli", "default_chain", local_chain["name"])
    return Chain.seed_one(local_chain)


def seed_chains(app: Web3Cli, chains: List[ChainSeed]) -> List[Chain]:
    """Add the given seed chains to the database"""
    db_ready_or_raise(app)
    return Chain.seed(chains)


def seed_local_chain(app: Web3Cli, make_default: bool = True) -> Chain:
    """Add the local network as a chain, with label local_chain, and
    make it the default network"""
    return seed_chain(app, local_chain, make_default)


def seed_addresses(
    app: Web3Cli, addresses: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """Add the given fixture addresses to the database"""
    db_ready_or_raise(app)
    for a in addresses:
        Address.create(
            label=a["label"],
            address=a["address"],
            description=a.get("description"),
        )
    return addresses


def seed_signers(app: Web3Cli, signers: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Add the given fixture signers to the database"""
    db_ready_or_raise(app)
    for s in signers:
        Signer.create_encrypt(label=s["label"], key=s["private_key"], pwd=app.app_key)
    return signers


def seed_accounts(
    app: Web3Cli,
    accounts: List[Account],
    accounts_keys: List[str],
    default_signer: str = None,
) -> List[Account]:
    """Create a signer for each of the given brownie accounts,
    with numeric labels: s0, s1, s2, etc.

    Accounts 0 and 1 will be added a second time with labels 'alice'
    and 'bob', respectively.

    Optionally, set one of the accounts to be the default signer."""
    db_ready_or_raise(app)
    # Create alice and bob signers
    Signer.create_encrypt(label="alice", key=accounts_keys[0], pwd=app.app_key)
    Signer.create_encrypt(label="bob", key=accounts_keys[1], pwd=app.app_key)
    # Create signers with labels s0, s1, s2, ...
    for i, account in enumerate(accounts):
        signer = Signer.create_encrypt(
            label=f"s{i}", key=accounts_keys[i], pwd=app.app_key
        )
        # Verify signer addresses
        if signer.address != account.address:
            raise Web3CliError("Mismatch between brownie accounts and signers")
    # Optionally set default signer
    if default_signer:
        app.config.set("web3cli", "default_signer", default_signer)
    return accounts
