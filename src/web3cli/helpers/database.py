from cement import App
from web3cli.core.exceptions import Web3CliError
from web3cli.core.helpers.database import tables
import os


def db_ready_or_raise(app: App) -> None:
    """Check whether the DB is attached to the app and connected"""
    if not app.db.is_connection_usable():
        raise Web3CliError("Could not establish database connection")


def get_db_file(app: App) -> str:
    """Return the full path of the database file, from
    the configuration"""
    return os.path.expanduser(app.config.get("web3cli", "db_file"))


def maybe_delete_db_file(app: App) -> None:
    """Delete the database file if app.delete_db is True"""
    if app.delete_db:
        delete_db_file(app)


def delete_db_file(app: App) -> None:
    """Delete the database file"""
    file = get_db_file(app)
    if os.path.isfile(file):
        os.remove(file)


def truncate_tables(app: App) -> None:
    """Empty all tables in the database"""
    db_ready_or_raise(app)
    for table in tables:
        table.delete().execute()
