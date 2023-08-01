from typing import Any

from cement import App as CementApp

from web3cli import helpers
from web3core.models.chain import Chain, Rpc
from web3core.models.signer import Signer


class App(CementApp):
    """App object with some extra methods with respect to Cement
    default app; subclass this to define new apps."""

    def __init__(self, *args: Any, **kw: Any) -> None:
        """For mypy"""
        super().__init__(*args, **kw)
        self.signer: Signer
        self.chain: Chain
        self.rpc: Rpc
        self.priority_fee: int

    def get_option(self, option: str) -> Any:
        """Shorthand to access app options"""
        return helpers.config.get_option(self, option)

    def set_option(self, option: str, value: Any) -> Any:
        """Shorthand to set app options"""
        return helpers.config.set_option(self, option, value)
