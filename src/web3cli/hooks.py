"""Functions called at specific points of the app lifecylce"""

import ast
import secrets
from os.path import isfile

import cement
from cement import App
from genericpath import isfile

from web3cli.helpers.config import update_setting_in_config_file
from web3cli.helpers.database import get_db_file
from web3core.db import DB
from web3core.helpers.database import init_db
from web3core.helpers.seed import populate_db
from web3core.models import MODELS

####################
# Register hooks
####################


def post_setup(app: App) -> None:
    """Callback to the post_setup hook, which is fired at the end
    of app.setup(), as soon as the app has finished parsing the
    configuration files, and before app.run(), where the CLI command
    will be run"""
    customize_extensions(app)
    maybe_create_app_key(app)
    init_and_attach_db(app)


def post_argument_parsing(app: App) -> None:
    """Callback to the post_argument_parsing hook, which is fired
    as one of the first steps of app.run(), after app.setup() has
    completed."""
    pass


####################
# Implementation
####################


def init_and_attach_db(app: App) -> None:
    """Attach the production database to the app object, so that the
    controllers can access it. If the database file does not exist,
    create it and seed it"""
    db_path = get_db_file(app)
    do_populate = (
        not isfile(db_path) and app.config.get("web3cli", "populate_db") == True
    )
    if not isfile(db_path):
        app.log.debug("Creating database...")
    app.extend("db", init_db(DB, MODELS, db_path))
    if do_populate:
        populate_db()


def maybe_create_app_key(app: App) -> None:
    """Create an app key if it does not exist already;
    extend the app object with the app key"""
    if not app.config.get("web3cli", "app_key"):
        new_key = secrets.token_bytes(32)
        update_setting_in_config_file(
            app,
            setting="app_key",
            value=str(new_key),
            do_log=False,
            is_global=True,
        )
        app.config.set("web3cli", "app_key", str(new_key))

    # Create the shortcut app.app_key
    key = app.config.get("web3cli", "app_key")
    app.extend("app_key", ast.literal_eval(key))


def customize_extensions(app: App) -> None:
    """Customize the behaviour of cement extensions
    (https://docs.builtoncement.com/core-foundation/extensions-1)"""
    # Set the output format for tables
    cement.ext.ext_tabulate.TabulateOutputHandler.Meta.format = app.config.get(
        "web3cli", "output_table_format"
    )
