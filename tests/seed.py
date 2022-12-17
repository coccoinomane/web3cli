"""Please note this file DOES NOT contain tests, but
helper functions to better run tests"""

from typing import List

from brownie.network.account import Account

from web3cli.core.exceptions import Web3CliError
from web3cli.core.models.chain import Chain
from web3cli.core.models.signer import Signer
from web3cli.core.seeds import chain_seeds
from web3cli.helpers.database import db_ready_or_raise
from web3cli.helpers.seed import seed_chain
from web3cli.main import Web3Cli


def seed_local_chain(app: Web3Cli, make_default: bool = True) -> Chain:
    """Add the local network as a chain, with name 'local' and
    make it the default network"""
    return seed_chain(app, chain_seeds.local, make_default)


def seed_local_accounts(
    app: Web3Cli,
    accounts: List[Account],
    accounts_keys: List[str],
    default_signer: str = None,
) -> List[Account]:
    """Create a signer for each of the given brownie accounts,
    with numeric names: s0, s1, s2, etc.

    Accounts 0 and 1 will be added a second time with names 'alice'
    and 'bob', respectively.

    Optionally, set one of the accounts to be the default signer."""
    db_ready_or_raise(app)
    # Create alice and bob signers
    Signer.create_encrypt(name="alice", key=accounts_keys[0], pwd=app.app_key)
    Signer.create_encrypt(name="bob", key=accounts_keys[1], pwd=app.app_key)
    # Create signers with names s0, s1, s2, ...
    for i, account in enumerate(accounts):
        signer = Signer.create_encrypt(
            name=f"s{i}", key=accounts_keys[i], pwd=app.app_key
        )
        # Verify signer addresses
        if signer.address != account.address:
            raise Web3CliError("Mismatch between brownie accounts and signers")
    # Optionally set default signer
    if default_signer:
        app.config.set("web3cli", "default_signer", default_signer)
    return accounts
