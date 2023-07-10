"""Helper functions to populate the DB for the tests"""

from typing import List

import ape
from web3cli.exceptions import Web3CliError
from web3cli.helpers.database import db_ready_or_raise
from web3cli.main import Web3Cli
from web3core.helpers.seed import seed_chain
from web3core.models.chain import Chain
from web3core.models.contract import Contract
from web3core.models.signer import Signer
from web3core.seeds import chain_seeds


def seed_local_chain(app: Web3Cli, chain_name: str, make_default: bool = True) -> Chain:
    """Add the given local chain to the DB and make it the default network"""
    chain = seed_chain(getattr(chain_seeds, f"{chain_name}"))
    if make_default:
        app.set_option("default_chain", chain.name)
    return chain


def seed_local_accounts(
    app: Web3Cli,
    accounts: ape.managers.accounts.AccountManager,
    accounts_keys: List[str],
    default_signer: str = None,
) -> ape.managers.accounts.AccountManager:
    """Create a signer for each of the given ape accounts,
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
            raise Web3CliError("Mismatch between ape accounts and signers")
    # Optionally set default signer
    if default_signer:
        app.set_option("default_signer", default_signer)
    return accounts


def seed_local_contract(
    app: Web3Cli,
    name: str,
    ape_contract: ape.contracts.ContractInstance,
    type: str = None,
    chain_name: str = None,
) -> Contract:
    """Create a contract in the DB for the given Brownie contract.

    If you specify the contract type, that type's ABI will override
    the ABI stored in the Brownie contract."""
    db_ready_or_raise(app)
    return Contract.create(
        name=name,
        desc=f"'{name}' contract imported from ape",
        chain=chain_name or app.get_option("default_chain"),
        address=ape_contract.address,
        type=type,
        abi=None if type else ape_contract.contract_type.dict()["abi"],
    )


def seed_local_token(
    app: Web3Cli, token: ape.contracts.ContractInstance, chain_name: str = None
) -> Contract:
    """Create a contract in the DB for the given Brownie token"""
    db_ready_or_raise(app)
    return Contract.create(
        name=token.symbol().lower(),
        desc=token.name(),
        chain=chain_name or app.get_option("default_chain"),
        address=token.address,
        type="erc20",
        abi=token.contract_type.dict()["abi"],
    )
