from __future__ import annotations
from typing import Any, List
from peewee import TextField, IntegerField, ForeignKeyField
from web3cli.core.exceptions import ChainNotFound, RpcIsInvalid, Web3CliError
from web3cli.core.helpers.chains import is_rpc_uri_valid
from web3cli.core.models.base_model import BaseModel
from web3.types import Middleware
from web3.middleware import geth_poa_middleware
from web3cli.core.models.types import ChainFields
from web3cli.core.seeds.types import ChainSeed
from web3cli.core.types import Logger


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
    def upsert(cls, fields: ChainFields, logger: Any = lambda msg: None) -> Chain:
        """Create a chain, or replace it if a chain with the same
        name already exists, maintaining its ID and relations."""

        # Create or update chain
        chain: Chain = Chain.get_or_none(name=fields["name"])
        if chain:
            Chain.update(**fields).where(Chain.id == chain.id).execute()
            chain = Chain.get(id=chain.id)
            logger(f"Chain {chain.name} updated")
        else:
            chain = Chain.create(**fields)
            logger(f"Chain {chain.name} created")
        return chain

    @classmethod
    def seed_one(
        cls, seed_chain: ChainSeed, logger: Logger = lambda msg: None
    ) -> Chain:
        """Create a chain and its RPCs in the db.

        If a chain with the same already exists, it will be
        replaced and any new RPC added."""

        # Create or update chain
        chain_fields: ChainFields = {
            "name": seed_chain["name"],
            "chain_id": seed_chain["chain_id"],
            "coin": seed_chain["coin"],
            "tx_type": seed_chain["tx_type"],
            "middlewares": ",".join(seed_chain["middlewares"]) or None,
        }
        chain = Chain.upsert(chain_fields, logger)

        # Create the rpcs
        for seed_rpc in seed_chain["rpcs"]:
            chain.add_rpc(seed_rpc, logger)

        return chain

    @classmethod
    def seed(
        cls, seed_chains: List[ChainSeed], logger: Any = lambda msg: None
    ) -> List[Chain]:
        """Populate the table with the given list of chains
        and RPCs, and return the list of created instances.

        For any given chain, if a chain with the same already exists,
        it will be replaced and any new RPC added."""
        return [Chain.seed_one(seed_chain, logger) for seed_chain in seed_chains]

    @classmethod
    def parse_middleware(cls, middleware: str) -> Middleware:
        try:
            return {
                "geth_poa_middleware": geth_poa_middleware,
            }[middleware]
        except:
            raise Web3CliError(f"Middleware {middleware} not supported")

    def add_rpc(self, rpc_url: str, logger: Logger = lambda msg: None) -> Rpc:
        """Add an RPC to a chain.

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


class Rpc(BaseModel):
    class Meta:
        table_name = "rpcs"

    url = TextField()


class ChainRpc(BaseModel):
    class Meta:
        table_name = "chain_rpc"

    chain = ForeignKeyField(Chain, on_delete="CASCADE")
    rpc = ForeignKeyField(Rpc, on_delete="CASCADE")
