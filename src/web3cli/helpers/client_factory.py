from cement import App
from web3cli.core.helpers.client_factory import make_base_client, make_base_wallet
from web3client.base_client import BaseClient
from web3cli.helpers import args
from web3cli.core.exceptions import SignerNotFound


def make_client(app: App, log: bool = False) -> BaseClient:
    """Client suitable to read the blockchain"""
    if log:
        app.log.info(f"Using chain '{app.chain}'")
    return make_base_client(app.chain)


def make_wallet(app: App, log: bool = False) -> BaseClient:
    """Client suitable to read and write to the blockchain"""
    if not app.signer:
        raise SignerNotFound(
            "Could not find a signer: create one with `web3 signer add`"
        )
    client = make_base_wallet(app.chain, app.signer, app.app_key)
    if log:
        app.log.info(f"Using signer '{app.signer}' on chain '{app.chain}")
    return client
