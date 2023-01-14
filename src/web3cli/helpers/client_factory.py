from typing import Any

from cement import App
from web3.types import ABI
from web3client.base_client import BaseClient

from web3cli.exceptions import Web3CliError
from web3core.helpers.client_factory import make_base_client, make_base_wallet
from web3core.helpers.client_factory import (
    make_contract_wallet as make_contract_wallet_,
)
from web3core.models.contract import Contract


def make_client(app: App, log: bool = False, **client_args: Any) -> BaseClient:
    """Client suitable to read from the blockchain"""
    return make_base_client(
        chain=app.chain,
        node_uri=app.rpc,
        logger=app.log.info if log else None,
        **client_args,
    )


def make_wallet(app: App, log: bool = False, **client_args: Any) -> BaseClient:
    """Client suitable to read from and write to the blockchain"""
    return make_base_wallet(
        chain=app.chain,
        signer_name=app.signer,
        password=app.app_key,
        node_uri=app.rpc,
        logger=app.log.info if log else app.log.info if log else None,
        **client_args,
    )


def make_contract_wallet(
    app: App,
    contract_name: str,
    contract_type: str = None,
    log: bool = False,
    **client_args: Any,
) -> BaseClient:
    """Client suitable to interact with the given smart contract"""
    # Fetch contract
    contract = Contract.get_by_name_and_chain_or_raise(
        contract_name.lower(), app.chain_name
    )
    if contract.type != contract_type:
        raise Web3CliError(f"Contract '{contract_name}' not of type '{contract_type}'")
    return make_contract_wallet_(
        contract_name=contract_name,
        chain=app.chain,
        signer_name=app.signer,
        password=app.app_key,
        node_uri=app.rpc,
        logger=app.log.info if log else app.log.info if log else None,
        **client_args,
    )


def make_erc20_wallet(
    app: App, token_name: str, log: bool = False, **client_args: Any
) -> BaseClient:
    """Client suitable to interact with the given ERC20 token"""
    return make_contract_wallet(app, token_name, "erc20", log, **client_args)
