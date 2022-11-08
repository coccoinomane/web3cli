"""Please note this file DOES NOT contain tests, but
helper functions to better run tests"""

from web3cli.main import Web3Cli
from web3cli.core.helpers import yaml
from typing import Any, Dict
import os


def get_config_filepath() -> str:
    """Path to the config file that the app will use while running tests"""
    return os.path.join(
        os.path.expanduser("~"), ".web3cli", "config", "web3cli_test.yml"
    )


def delete_configuration_file(app: Web3Cli) -> None:
    """Delete the configuration file for the test app"""
    file = get_config_filepath()
    if os.path.isfile(file):
        os.remove(file)


def set_config(setting: str, value: Any) -> None:
    """Set a default_signer in the test config file and return the test signer"""
    yaml.set(
        filepath=get_config_filepath(),
        setting=setting,
        value=value,
        logger=None,
        section="web3cli",
    )
