import os
from typing import List, Type

from playhouse.sqlite_ext import SqliteExtDatabase

from web3core.helpers.os import create_folder
from web3core.models.address import Address
from web3core.models.base_model import BaseModel, db
from web3core.models.chain import Chain, ChainRpc, Rpc
from web3core.models.contract import Contract
from web3core.models.signer import Signer
from web3core.models.tx import Tx

tables: List[Type[BaseModel]] = [Signer, Address, Chain, Rpc, ChainRpc, Tx, Contract]


def init_db(db_path: str) -> SqliteExtDatabase:
    """Connect the global database object (db) to the given database file.
    If the database file does not exist, a new database file will be created
    at the given path, along with its parent folders."""
    db_path = os.path.expanduser(db_path)
    create_folder(os.path.dirname(db_path), 0o744)
    db.init(db_path)
    db.connect()
    db.create_tables(tables)
    return db
