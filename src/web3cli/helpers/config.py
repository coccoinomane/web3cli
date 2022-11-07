from cement import App
from typing import Any
from web3cli.core.helpers import yaml


def update_setting(
    app: App, setting: str, value: Any, do_log: False, is_global: bool = True
):
    """Update the value of a setting in the configuration file.
    If is_global is True, update the global configuration file,
    otherwise update the one in the directory from where the script
    was launched.

    If the file does not exist, it will be created."""

    filepath = app.Meta.config_files[0] if is_global else app.Meta.config_files[-1]

    yaml.set(
        filepath=filepath,
        setting=setting,
        value=value,
        logger=app.log if do_log else None,
        section="web3cli",
    )


def get_local_configuration_file(app: App) -> str:
    """Return the path of the local configuration file. Please
    note that the local configuration file might not exist
    even if it does"""
    return app.Meta.config_files[-1]


def get_local_configuration_file(app: App) -> str:
    """Return the path of the local configuration file"""
    return app.Meta.config_files[-1]
