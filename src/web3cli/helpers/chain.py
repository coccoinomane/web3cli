from cement import App

from web3cli.core.exceptions import ChainNotFound
from web3cli.core.models.chain import Chain


def chain_ready_or_raise(app: App) -> None:
    """Check whether the app is ready to access the blockchain"""
    if not type(app.chain) == Chain:
        raise ChainNotFound(f"Chain '{app.chain_name}' does not exist")
