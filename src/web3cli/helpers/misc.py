from cement import App
from web3cli.core.models.chain import Chain


def get_coin(app: App) -> str:
    """Return the native coin of the current chain"""
    return get_chain_instance(app).coin


def get_chain_instance(app: App) -> Chain:
    """Return the object representing the current chain"""
    return Chain.get_by_name_or_raise(app.chain)
