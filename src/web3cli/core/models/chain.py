from __future__ import annotations
from typing import List
from peewee import TextField, IntegerField, ForeignKeyField
from web3cli.core.exceptions import ChainNotFound, Web3CliError
from web3cli.core.models.base_model import BaseModel
from web3.types import Middleware
from web3.middleware import geth_poa_middleware
from web3cli.core.seeds.types import ChainSeed


class Chain(BaseModel):
    class Meta:
        table_name = "chains"

    name = TextField(unique=True)
    chain_id = IntegerField()
    coin = TextField()
    tx_type = IntegerField(default=2)
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

    @classmethod
    def seed(cls, seed_chains: List[ChainSeed]) -> List[Chain]:
        """Populate the table with the given list of chains
        and RPCs, and return the list of created instances.

        For any given chain, if a chain with the same
        already exists, it will be overwritten."""
        output = []
        for c in seed_chains:
            # Delete chain if it already exists in the db
            try:
                Chain.get_or_none(name=c["name"]).delete_instance(recursive=True)
            except:
                pass
            # Create chain in the db
            chain = Chain.create(
                name=c["name"],
                chain_id=c["chain_id"],
                coin=c["coin"],
                tx_type=c["tx_type"],
                middlewares=",".join(c["middlewares"]) or None,
            )
            output.append(chain)

            for seed_rpc in c["rpcs"]:
                # Delete RPC if it already exists in the db
                try:
                    Rpc.get_or_none(url=seed_rpc).delete_instance()
                except:
                    pass
                # Create RPC in the database
                rpc = Rpc.create(url=seed_rpc)

                # Create chain-rpc relation
                ChainRpc.create(chain=chain, rpc=rpc)
        return output

    @classmethod
    def parse_middleware(cls, middleware: str) -> Middleware:
        try:
            return {
                "geth_poa_middleware": geth_poa_middleware,
            }[middleware]
        except:
            raise Web3CliError(f"Middleware {middleware} not supported")


class Rpc(BaseModel):
    class Meta:
        table_name = "rpcs"

    url = TextField()


class ChainRpc(BaseModel):
    class Meta:
        table_name = "chain_rpc"

    chain = ForeignKeyField(Chain, on_delete="CASCADE")
    rpc = ForeignKeyField(Rpc, on_delete="CASCADE")
