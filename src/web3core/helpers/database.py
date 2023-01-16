import os
from typing import List

from playhouse.signals import Model
from playhouse.sqlite_ext import SqliteExtDatabase

from web3core.helpers.os import create_folder


def init_db(
    db: SqliteExtDatabase, models: List[Model], db_path: str = None
) -> SqliteExtDatabase:
    """Connect the global database object (db) to the given database file.
    If the database file does not exist, a new database file will be created
    at the given path, along with its parent folders."""
    if db_path != ":memory:":
        db_path = os.path.expanduser(db_path)
        create_folder(os.path.dirname(db_path), 0o744)
    db.init(db_path)
    db.connect()
    db.create_tables(models)
    return db
