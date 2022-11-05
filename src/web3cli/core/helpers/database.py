from peewee import SqliteDatabase
from web3cli.core.models.base_model import db
from web3cli.core.models.addresses import Addresses
from web3cli.core.helpers.os import create_folder
import os


def init_db(db_path: str) -> SqliteDatabase:
    """Connect the global database object (db) to the given database file.
    If the database file does not exist, a new database file will be created
    at the given path, along with its parent folders."""
    db_path = os.path.expanduser(db_path)
    create_folder(os.path.dirname(db_path), 0o744)
    db.init(db_path)
    db.connect()
    db.create_tables([Addresses])
    return db
