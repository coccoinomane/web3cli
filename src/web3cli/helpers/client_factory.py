from typing import Any, Type
from cement import App
from web3cli.core.models.signer import Signer
from web3cli.helpers.crypto import decrypt_string_with_app_key
from web3client.base_client import BaseClient
from web3cli.helpers import args
from web3cli.core.exceptions import SignerNotFound
import web3factory.factory
from web3cli.core.models.chain import Chain


def make_client(app: App, log: bool = False) -> BaseClient:
    """Client suitable to read the blockchain"""
    args.validate_chain(app.chain)
    if log:
        app.log.info(f"Using chain '{app.chain}'")
    return web3factory.factory.make_client(app.chain)


def make_wallet(app: App, log: bool = False) -> BaseClient:
    """Client suitable to read and write to the blockchain"""
    client = make_client(app, log)
    if not app.signer:
        raise SignerNotFound(
            "Could not find a signer. Create one with `web3 signer add <label>` and/or pick one with `web3 --signer <label> ..."
        )
    signer = Signer.get_by_label_or_raise(app.signer)
    if log:
        app.log.info(f"Using signer '{app.signer}'")
    client.setAccount(decrypt_string_with_app_key(app, signer.key))
    return client


# def make_base_client(
#     chain_name: str,
#     node_uri: str = None,
#     base: Type[BaseClient] = BaseClient,
#     **clientArgs: Any,
# ) -> BaseClient:
#     """
#     Return a brand new client configured for the given blockchain
#     """
#     chain = Chain.get_by_name_or_raise(chain_name)
#     if nodeUri is None:
#         nodeUri = pick_rpc(networkName)
#     client = base(nodeUri=nodeUri, **clientArgs)
#     client.chainId = networkConfig["chainId"]
#     client.txType = networkConfig["txType"]
#     client.setMiddlewares(networkConfig.get("middlewares", []))

#     return client
