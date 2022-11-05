from cement import App
from web3cli.core.helpers.database import init_db
import os


def attach_production_db(app: App) -> None:
    """Attach the production database to the app object, so that the
    controllers can access it"""
    db_path = os.path.expanduser(app.config.get("web3cli", "db_file"))
    app.extend("db", init_db(db_path))


def attach_testing_db(app: App) -> None:
    """Empty the testing database and attach it to the app object, so
    that the controllers can access it."""
    db_path = os.path.expanduser(app.config.get("web3cli_test", "db_file"))
    if os.path.isfile(db_path):
        os.remove(db_path)  # important!
    app.extend("db", init_db(db_path))
