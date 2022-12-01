from typing import Any, Type
from web3cli.core.models.signer import Signer
from web3cli.core.types import Logger
from web3client.base_client import BaseClient
from web3cli.core.models.chain import Chain
from web3cli.core.helpers.crypto import decrypt_string


def make_base_client(
    chain_name: str,
    node_uri: str = None,
    base: Type[BaseClient] = BaseClient,
    logger: Logger = lambda msg: None,
    **clientArgs: Any,
) -> BaseClient:
    """Return a brand new client configured for the given blockchain"""
    chain: Chain = Chain.get_by_name_or_raise(chain_name)
    if node_uri is None:
        node_uri = chain.pick_rpc().url
    if logger:
        logger(f"Using chain {chain_name} with RPC {node_uri}")
    client = base(nodeUri=node_uri, **clientArgs)
    client.chainId = chain.chain_id
    client.txType = chain.tx_type
    middlewares = chain.middlewares.split(",") if chain.middlewares else []
    client.setMiddlewares([Chain.parse_middleware(m) for m in middlewares])
    return client


def make_base_wallet(
    chain_name: str,
    signer_name: str,
    password: bytes,
    node_uri: str = None,
    base: Type[BaseClient] = BaseClient,
    logger: Logger = lambda msg: None,
    **clientArgs: Any,
) -> BaseClient:
    """Return a brand new client configured for the given blockchain,
    with signing support. You need to provide the name of the signer
    from the DB, and a password to decrypt the signer's key."""
    client = make_base_client(chain_name, node_uri, base, **clientArgs)
    if logger:
        logger(f"Using signer {signer_name}")
    signer = Signer.get_by_name_or_raise(signer_name)
    client.setAccount(decrypt_string(signer.key, password))
    return client
