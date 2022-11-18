from __future__ import annotations
from peewee import TextField, IntegerField, ForeignKeyField
from web3cli.core.exceptions import ChainNotFound
from web3cli.core.models.base_model import BaseModel
import web3


class Chain(BaseModel):
    class Meta:
        table_name = "chains"

    name = TextField(unique=True)
    chain_id = IntegerField()
    coin = TextField()
    middlewares = TextField(null=True)

    @classmethod
    def get_by_name(cls, name: str) -> Chain:
        """Return the chain object with the given name, or None if
        it does not exist"""
        return cls.get_or_none(cls.name == name)

    @classmethod
    def get_by_name_or_raise(cls, name: str) -> Chain:
        """Return the chain object with the given name; raise
        error if it does not exist"""
        try:
            return cls.get(cls.name == name)
        except:
            raise ChainNotFound(f"Chain '{name}' does not exist")


class Rpc(BaseModel):
    class Meta:
        table_name = "rpcs"

    url = TextField()


class ChainRpc(BaseModel):
    class Meta:
        table_name = "chain_rpc"

    chain = ForeignKeyField(Chain)
    rpc = ForeignKeyField(Rpc)
