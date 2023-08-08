from logging import Logger
from typing import Any, List

from cement import App as CementApp
from peewee import Model, SqliteDatabase

from web3cli import helpers
from web3core.models.chain import Chain, Rpc
from web3core.models.signer import Signer


class App(CementApp):
    """App object with some extra methods with respect to Cement
    default app; subclass this to define new apps."""

    def __init__(self, *args: Any, **kw: Any) -> None:
        """For mypy"""
        super().__init__(*args, **kw)
        self.app_key: bytes
        self.log: Logger
        self.signer: Signer
        self.chain: Chain
        self.rpc: Rpc
        self.priority_fee: int
        self.db: SqliteDatabase
        self.models: List[Model]

    def get_option(self, option: str) -> Any:
        """Shorthand to access app options"""
        return helpers.config.get_option(self, option)

    def set_option(self, option: str, value: Any) -> Any:
        """Shorthand to set app options"""
        return helpers.config.set_option(self, option, value)
