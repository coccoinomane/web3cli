"""Functions called at specific points of the app lifecylce"""

import ast
import secrets
from os.path import isfile

import cement
from genericpath import isfile

from web3cli.framework.app import App
from web3cli.helpers.config import update_setting_in_config_file
from web3cli.helpers.database import get_db_filepath
from web3core.helpers.database import init_db
from web3core.helpers.seed import populate_db

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
    create it and optionally seed it"""

    # Continue only if db instance and models are defined in the app meta
    if not hasattr(app._meta, "db_instance") or not hasattr(app._meta, "db_models"):
        return

    # Extend the app with the db instance and models
    app.extend("db", app._meta.db_instance)
    app.extend("models", app._meta.db_models)

    # Create the database and populate it if it does not exist
    db_path = get_db_filepath(app)
    do_populate = not isfile(db_path) and app.get_option("populate_db") == True
    if not isfile(db_path):
        app.log.debug("Creating database...")
    init_db(app.db, app.models, db_path)

    # Populate database if needed
    if do_populate:
        populate_db()


def maybe_create_app_key(app: App) -> None:
    """Create an app key if it does not exist already;
    extend the app object with the app key"""
    if not app.get_option("app_key"):
        new_key = secrets.token_bytes(32)
        update_setting_in_config_file(
            app,
            setting="app_key",
            value=str(new_key),
            do_log=False,
            is_global=True,
        )
        app.set_option("app_key", str(new_key))

    # Create the shortcut app.app_key
    key = app.get_option("app_key")
    app.extend("app_key", ast.literal_eval(key))


def customize_extensions(app: App) -> None:
    """Customize the behaviour of cement extensions
    (https://docs.builtoncement.com/core-foundation/extensions-1)"""
    # Set the output format for tables
    cement.ext.ext_tabulate.TabulateOutputHandler.Meta.format = app.get_option(
        "output_table_format"
    )
