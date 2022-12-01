from cement import App
from typing import Any
from web3cli.core.helpers import yaml
from web3cli.core.helpers.os import create_folder
import os


def update_setting_in_config_file(
    app: App, setting: str, value: Any, do_log: bool = False, is_global: bool = True
) -> None:
    """Update the value of a setting in the configuration file.
    If is_global is True, update the global configuration file,
    otherwise update the one in the directory from where the script
    was launched.

    If the file does not exist, it will be created, along with its
    parent folders"""

    filepath = (
        get_global_configuration_file(app)
        if is_global
        else get_local_configuration_file(app)
    )

    if is_global:
        create_folder(os.path.dirname(filepath), 0o744)

    yaml.set(
        filepath=filepath,
        setting=setting,
        value=value,
        logger=app.log.info if do_log else None,
        section="web3cli",
    )


def get_local_configuration_file(app: App) -> str:
    """Return the path of the local configuration file"""
    return app.Meta.config_files[-1]


def get_global_configuration_file(app: App) -> str:
    """Return the path of the global configuration file"""
    return app.Meta.config_files[0]
