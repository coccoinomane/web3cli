from cement import App
from web3cli.core.helpers.database import init_db
import os


def attach_db(app: App) -> None:
    """Attach the production database to the app object, so that the
    controllers can access it"""
    db_path = get_db_file(app)
    app.extend("db", init_db(db_path))


def get_db_file(app: App) -> str:
    """Return the full path of the database file, from
    the configuration"""
    return os.path.expanduser(app.config.get("web3cli", "db_file"))


def delete_db_file(app: App) -> None:
    """Delete the database file"""
    file = get_db_file(app)
    if os.path.isfile(file):
        os.remove(file)
