from __future__ import annotations

from typing import List

from peewee import ForeignKeyField, IntegerField, TextField
from playhouse.shortcuts import dict_to_model
from web3.middleware import geth_poa_middleware
from web3.types import Middleware

from web3core.exceptions import (
    ChainNotResolved,
    RpcIsInvalid,
    RpcNotFound,
    Web3CoreError,
)
from web3core.helpers.rpc import is_rpc_uri_valid
from web3core.models.base_model import BaseModel
from web3core.models.types import ChainFields
from web3core.seeds import chain_seeds
from web3core.types import Logger


class Chain(BaseModel):
    class Meta:
        table_name = "chains"

    name = TextField(unique=True)
    desc = TextField(null=True)
    chain_id = IntegerField()
    coin = TextField()
    tx_type = IntegerField(default=2)
    middlewares = TextField(null=True)

    @classmethod
    def upsert(cls, fields: ChainFields, logger: Logger = None) -> Chain:
        """Create chain or update it if one with the same name already exists"""
        return cls.upsert_by_field(cls.name, fields["name"], fields, logger, True)

    @classmethod
    def seed_one(cls, seed: ChainFields, logger: Logger = lambda msg: None) -> Chain:
        """Create a chain and its RPCs in the db; if a chain with the
        same already exists, it will be replaced and new RPCs added."""
        chain = Chain.upsert(seed, logger)
        for seed_rpc in seed["rpcs"]:
            chain.add_rpc(seed_rpc["url"], logger)
        return chain

    @classmethod
    def seed(
        cls, seeds: List[ChainFields], logger: Logger = lambda msg: None
    ) -> List[Chain]:
        """Populate the table with the given list of chains
        and RPCs, and return the list of created instances."""
        return [Chain.seed_one(seed, logger) for seed in seeds]

    @classmethod
    def parse_middleware(cls, middleware: str) -> Middleware:
        """Given the name of a Web3 middleware (e.g. geth_poa_middleware)
        return the corresponding Middleware function"""
        try:
            return {
                "geth_poa_middleware": geth_poa_middleware,
            }[middleware]
        except:
            raise Web3CoreError(f"Middleware {middleware} not supported")

    @classmethod
    def resolve_chain(cls, name: str) -> Chain:
        """Return the chain with the given name, looking first in
        the database and then in the seed chains. If not found, raise
        ChainNotResolved."""
        # Look in the DB
        chain = Chain.get_by_name(name)
        if chain:
            return chain

        # Look in the seeds
        for c in chain_seeds.all:
            if c["name"] == name:
                return dict_to_model(Chain, c, True)

        raise ChainNotResolved(
            f"Could not find chain '{name}', add it with `w3 db chain add`"
        )

    def add_rpc(self, rpc_url: str, logger: Logger = lambda msg: None) -> Rpc:
        """Add an RPC to the chain instance.

        The RPC will be created in its own table, if it does not exist
        yet, and linked to the chain via the pivot table chain_rpc"""
        # Validate RPC
        if not is_rpc_uri_valid(rpc_url):
            raise RpcIsInvalid(f"RPC not valid or not supported: {rpc_url}")

        # Create the rpcs
        rpc_params = {"url": rpc_url}
        rpc: Rpc = Rpc.get_or_none(url=rpc_url)
        if not rpc:
            rpc = Rpc.create(**rpc_params)
            logger(f"Rpc {rpc.url} created")

        # Create the chain-rpc relation
        chain_rpc_params = {"chain": self, "rpc": rpc}
        chain_rpc: ChainRpc = ChainRpc.get_or_none(**chain_rpc_params)
        if not chain_rpc:
            chain_rpc = ChainRpc.create(**chain_rpc_params)
            logger(f"Rpc {rpc.url} connected to chain {self.name}")

        return rpc

    def get_rpcs(self) -> List[Rpc]:
        """Return the rpcs associated to the chain instance"""
        query = Rpc.select().join(ChainRpc).join(Chain).where(Chain.id == self.id)
        return [r for r in query]

    def pick_rpc(self) -> Rpc:
        """Return an RPC compatible with the chain instance. For now, just return
        the first RPC compatible with the chain, at some point, will implement some
        form of strategy here."""
        rpcs = self.get_rpcs()
        if not rpcs:
            raise RpcNotFound(f"Could not find a suitable RPC for chain {self.name}")
        return rpcs[0]


class Rpc(BaseModel):
    class Meta:
        table_name = "rpcs"

    url = TextField()

    def get_chains(self) -> List[Chain]:
        """Return the chains associated to the rpc instance"""
        query = Chain.select().join(ChainRpc).join(Rpc).where(Rpc.id == self.id)
        return [c for c in query]


class ChainRpc(BaseModel):
    class Meta:
        table_name = "chain_rpc"

    chain = ForeignKeyField(Chain, on_delete="CASCADE")
    rpc = ForeignKeyField(Rpc, on_delete="CASCADE")
