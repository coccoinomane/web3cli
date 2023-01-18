from typing import Any

from cement import App
from web3client.base_client import BaseClient

from web3core.helpers.client_factory import make_base_client, make_base_wallet
from web3core.helpers.client_factory import (
    make_contract_client as make_contract_client_,
)
from web3core.helpers.client_factory import (
    make_contract_wallet as make_contract_wallet_,
)


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


def make_contract_client(
    app: App,
    contract_name: str,
    log: bool = False,
    **client_args: Any,
) -> BaseClient:
    """Client suitable to interact with the given smart contract"""
    return make_contract_client_(
        contract_name=contract_name,
        chain=app.chain,
        node_uri=app.rpc,
        logger=app.log.info if log else app.log.info if log else None,
        **client_args,
    )


def make_contract_wallet(
    app: App,
    contract_name: str,
    log: bool = False,
    **client_args: Any,
) -> BaseClient:
    """Client suitable to interact with the given smart contract"""
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
    return make_contract_wallet(app, token_name, log, **client_args)
