from typing import Any, Union, cast

from web3client.base_client import BaseClient

from web3cli.framework.app import App
from web3core.helpers.client_factory import make_base_client
from web3core.helpers.client_factory import (
    make_contract_client as make_contract_client_,
)
from web3core.helpers.client_factory import make_contract_client_from_address_and_abi
from web3core.models.contract import Contract


def make_client(app: App, log: bool = False, **client_args: Any) -> BaseClient:
    """Client suitable to read from the blockchain"""
    return cast(
        BaseClient,
        make_base_client(
            chain=app.chain,
            node_uri=app.rpc.url,
            logger=app.log.info if log else None,
            **client_args,
        ),
    )


def make_wallet(app: App, log: bool = False, **client_args: Any) -> BaseClient:
    """Client suitable to read from and write to the blockchain"""
    return make_base_client(
        chain=app.chain,
        signer=app.signer,
        password=app.app_key,
        node_uri=app.rpc.url,
        logger=app.log.info if log else None,
        **client_args,
    )


def make_contract_client(
    app: App,
    contract: Union[Contract, str],
    log: bool = False,
    **client_args: Any,
) -> BaseClient:
    """Client suitable to read from the given smart contract"""
    return make_contract_client_(
        contract=contract,
        chain=app.chain,
        node_uri=app.rpc.url,
        logger=app.log.info if log else None,
        **client_args,
    )


def make_contract_wallet(
    app: App,
    contract: Union[Contract, str],
    log: bool = False,
    **client_args: Any,
) -> BaseClient:
    """Client suitable to interact with the given smart contract"""
    return make_contract_client_(
        contract=contract,
        chain=app.chain,
        signer=app.signer,
        password=app.app_key,
        node_uri=app.rpc.url,
        logger=app.log.info if log else None,
        **client_args,
    )


def make_erc20_client_from_address(
    app: App, token_address: str, log: bool = False, **client_args: Any
) -> BaseClient:
    """Wrapper to make_contract_client that returns a contract
    client even if the contract is not saved at database."""
    return make_contract_client_from_address_and_abi(
        address=token_address,
        chain=app.chain,
        type="erc20",
        node_uri=app.rpc.url,
        logger=app.log.info if log else None,
        **client_args,
    )


def make_erc20_wallet_from_address(
    app: App, token_address: str, log: bool = False, **client_args: Any
) -> BaseClient:
    """Wrapper to make_contract_client that returns a contract
    wallet even if the contract is not saved at database."""
    return make_contract_client_from_address_and_abi(
        address=token_address,
        chain=app.chain,
        signer=app.signer,
        password=app.app_key,
        type="erc20",
        node_uri=app.rpc.url,
        logger=app.log.info if log else None,
        **client_args,
    )
