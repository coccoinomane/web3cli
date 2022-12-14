from typing import Any, Type

from web3client.base_client import BaseClient

from web3core.helpers.crypto import decrypt_string
from web3core.models.chain import Chain
from web3core.models.signer import Signer
from web3core.types import Logger


def make_base_client(
    chain: Chain,
    node_uri: str = None,
    base: Type[BaseClient] = BaseClient,
    logger: Logger = lambda msg: None,
    **client_args: Any,
) -> BaseClient:
    """Return a brand new client configured for the given blockchain"""
    if node_uri is None:
        node_uri = chain.pick_rpc().url
    if logger:
        logger(f"Using chain {chain.name} with RPC {node_uri}")
    client = base(nodeUri=node_uri, **client_args)
    client.chainId = chain.chain_id
    client.txType = chain.tx_type
    middlewares = chain.middlewares.split(",") if chain.middlewares else []
    client.setMiddlewares([Chain.parse_middleware(m) for m in middlewares])
    return client


def make_base_wallet(
    chain: Chain,
    signer_name: str,
    password: bytes,
    node_uri: str = None,
    base: Type[BaseClient] = BaseClient,
    logger: Logger = lambda msg: None,
    **client_args: Any,
) -> BaseClient:
    """Return a brand new client configured for the given blockchain,
    with signing support. You need to provide the name of the signer
    from the DB, and a password to decrypt the signer's key."""
    client = make_base_client(chain, node_uri, base, **client_args)
    signer = Signer.get_by_name_or_raise(signer_name)
    if logger:
        logger(f"Using signer {signer_name}")
    client.setAccount(decrypt_string(signer.key, password))
    return client
