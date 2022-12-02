from __future__ import annotations
from typing import List
from peewee import TextField, IntegerField, ForeignKeyField
from web3cli.core.exceptions import (
    ChainNotFound,
    RpcIsInvalid,
    RpcNotFound,
    Web3CliError,
)
from web3cli.core.helpers.rpc import is_rpc_uri_valid
from web3cli.core.models.base_model import BaseModel
from web3.types import Middleware
from web3.middleware import geth_poa_middleware
from web3cli.core.models.types import ChainFields
from web3cli.core.types import Logger
from playhouse.shortcuts import update_model_from_dict


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
    def upsert(cls, fields: ChainFields, logger: Logger = None) -> Chain:
        """Create a chain, or replace it if a chain with the same
        name already exists, maintaining its ID and relations."""
        chain: Chain = Chain.get_or_none(name=fields["name"])
        if chain:
            chain = update_model_from_dict(chain, fields)
            if logger:
                logger(f"Chain {chain.name} updated")
        else:
            chain = Chain(**fields)
            if logger:
                logger(f"Chain {chain.name} created")
        chain.save()
        return chain

    @classmethod
    def seed_one(
        cls, seed_chain: ChainFields, logger: Logger = lambda msg: None
    ) -> Chain:
        """Create a chain and its RPCs in the db; if a chain with the
        same already exists, it will be replaced and new RPCs added."""
        chain = Chain.upsert(seed_chain, logger)
        for seed_rpc in seed_chain["rpcs"]:
            chain.add_rpc(seed_rpc["url"], logger)
        return chain

    @classmethod
    def seed(
        cls, chain_seeds: List[ChainFields], logger: Logger = lambda msg: None
    ) -> List[Chain]:
        """Populate the table with the given list of chains
        and RPCs, and return the list of created instances."""
        return [Chain.seed_one(chain_seed, logger) for chain_seed in chain_seeds]

    @classmethod
    def parse_middleware(cls, middleware: str) -> Middleware:
        """Given the name of a Web3 middleware (e.g. geth_poa_middleware)
        return the corresponding Middleware function"""
        try:
            return {
                "geth_poa_middleware": geth_poa_middleware,
            }[middleware]
        except:
            raise Web3CliError(f"Middleware {middleware} not supported")

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
