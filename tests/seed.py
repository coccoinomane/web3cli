"""Helper functions to populate the DB for the tests"""

from typing import List

from brownie.network.account import Account as BrownieAccount
from brownie.network.contract import Contract as BrownieContract
from web3cli.exceptions import Web3CliError
from web3cli.helpers.database import db_ready_or_raise
from web3cli.main import Web3Cli
from web3core.helpers.seed import seed_chain
from web3core.models.chain import Chain
from web3core.models.contract import Contract
from web3core.models.signer import Signer
from web3core.seeds import chain_seeds


def seed_local_chain(app: Web3Cli, make_default: bool = True) -> Chain:
    """Add the local network as a chain, with name 'local' and
    make it the default network"""
    chain = seed_chain(chain_seeds.local)
    if make_default:
        app.config.set("web3cli", "default_chain", chain.name)
    return chain


def seed_local_accounts(
    app: Web3Cli,
    accounts: List[BrownieAccount],
    accounts_keys: List[str],
    default_signer: str = None,
) -> List[BrownieAccount]:
    """Create a signer for each of the given brownie accounts,
    with numeric names: s0, s1, s2, etc.

    Accounts 0 and 1 will be added a second time with names 'alice'
    and 'bob', respectively.

    Optionally, set one of the accounts to be the default signer."""
    db_ready_or_raise(app)
    # Create alice and bob signers
    Signer.create_encrypt(name="alice", key=accounts_keys[0], pwd=app.app_key)
    Signer.create_encrypt(name="bob", key=accounts_keys[1], pwd=app.app_key)
    for i, account in enumerate(accounts):
        # Make sure keys are not exhausted
        if i >= len(accounts_keys):
            break
        # Create signers with names s0, s1, s2, ...
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


def seed_local_token(app: Web3Cli, token: BrownieContract) -> Contract:
    """Create a contract in the DB for the given Brownie token"""
    db_ready_or_raise(app)
    return Contract.create(
        name=token.symbol(),
        desc=token.name(),
        chain="local",
        address=token.address,
        type="erc20",
        abi=token.abi,
    )
