import os

from cement import App

from web3cli.exceptions import Web3CliError
from web3core.models import MODELS


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


def delete_db_file(app: App) -> bool:
    """Delete the database file; return True if the file was
    deleted, false if it was not found"""
    file = get_db_file(app)
    if os.path.isfile(file):
        os.remove(file)
        return True
    return False


def truncate_tables(app: App) -> None:
    """Empty all tables in the database"""
    db_ready_or_raise(app)
    for model in MODELS:
        model.delete().execute()
