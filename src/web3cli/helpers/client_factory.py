from cement import App
from web3cli.core.helpers.client_factory import make_base_client, make_base_wallet
from web3client.base_client import BaseClient
from web3cli.core.exceptions import SignerNotFound


def make_client(app: App, log: bool = False) -> BaseClient:
    """Client suitable to read from the blockchain"""
    return make_base_client(
        chain_name=app.chain, node_uri=app.rpc, logger=app.log.info if log else None
    )


def make_wallet(app: App, log: bool = False) -> BaseClient:
    """Client suitable to read from and write to the blockchain"""
    if not app.signer:
        raise SignerNotFound("Could not find a signer: create one with `w3 signer add`")
    return make_base_wallet(
        chain_name=app.chain,
        signer_name=app.signer,
        password=app.app_key,
        node_uri=app.rpc,
        logger=app.log.info if log else app.log.info if log else None,
    )
