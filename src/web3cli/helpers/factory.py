from cement import App
from web3client.base_client import BaseClient
import web3factory.factory
from web3cli.helpers import args


def make_client(app: App, log: bool = False) -> BaseClient:
    """Return a client to interact with the network provided
    by the user"""
    args.validate_network(app.network)
    if log:
        app.log.info(f"Using network '{app.network}'")
    return web3factory.factory.make_client(app.network)
