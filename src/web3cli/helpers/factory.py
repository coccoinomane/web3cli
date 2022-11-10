from cement import App
from web3cli.core.models.signer import Signer
from web3cli.helpers.crypto import decrypt_string_with_app_key
from web3client.base_client import BaseClient
import web3factory.factory
from web3cli.helpers import args


def make_client(app: App, log: bool = False) -> BaseClient:
    """Client suitable to read the blockchain"""
    args.validate_network(app.network)
    if log:
        app.log.info(f"Using network '{app.network}'")
    return web3factory.factory.make_client(app.network)


def make_wallet(app: App, log: bool = False) -> BaseClient:
    """Client suitable to read and write to the blockchain"""
    client = make_client(app, log)
    signer = Signer.get_by_label_or_raise(app.signer)
    if log:
        app.log.info(f"Using signer '{app.signer}'")
    client.setAccount(decrypt_string_with_app_key(app, signer.key))
    return client
