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
    def seed_one(cls, seed_chain: ChainSeed) -> Chain:
        """Create a chain and its RPCs in the db.

        If a chain with the same already exists, it will be
        replaced and any new RPC added."""

        # Create or update chain
        chain_params = {
            "name": seed_chain["name"],
            "chain_id": seed_chain["chain_id"],
            "coin": seed_chain["coin"],
            "tx_type": seed_chain["tx_type"],
            "middlewares": ",".join(seed_chain["middlewares"]) or None,
        }
        chain: Chain = Chain.get_or_none(name=seed_chain["name"])
        if chain:
            Chain.update(**chain_params).where(Chain.id == chain.id).execute()
            chain = Chain.get(id=chain.id)
        else:
            chain = Chain.create(**chain_params)

        print(chain.name)

        # Create the rpcs
        for seed_rpc in seed_chain["rpcs"]:
            rpc_params = {"url": seed_rpc}
            rpc: Rpc = Rpc.get_or_none(url=seed_rpc)
            if not rpc:
                rpc = Rpc.create(**rpc_params)

            # Create the chain-rpc relation
            chain_rpc_params = {"chain": chain, "rpc": rpc}
            chain_rpc: ChainRpc = ChainRpc.get_or_none(**chain_rpc_params)
            if not chain_rpc:
                chain_rpc = ChainRpc.create(**chain_rpc_params)

        return chain

    @classmethod
    def seed(cls, seed_chains: List[ChainSeed]) -> List[Chain]:
        """Populate the table with the given list of chains
        and RPCs, and return the list of created instances.

        For any given chain, if a chain with the same already exists,
        it will be replaced and any new RPC added."""
        return [Chain.seed_one(seed_chain) for seed_chain in seed_chains]

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
