from cement import App

from web3core.exceptions import ChainNotFound
from web3core.models.chain import Chain


def chain_ready_or_raise(app: App) -> None:
    """Check whether the app is ready to access the blockchain"""
    if not type(app.chain) == Chain:
        raise ChainNotFound(f"Chain '{app.chain_name}' does not exist")
