"""Please note this file DOES NOT contain tests, but
helper functions to better run tests"""

import secrets
import string
from web3cli.core.helpers import yaml
from typing import Any
from web3cli.main import Web3Cli
import os


def get_test_config_file() -> str:
    """Path to the config file that the app will use while running tests"""
    return os.path.join(
        os.path.expanduser("~"), ".web3cli", "config", "web3cli_test.yml"
    )


def delete_test_config_file(app: Web3Cli) -> None:
    """Delete the configuration file for the test app"""
    file = get_test_config_file()
    if os.path.isfile(file):
        os.remove(file)


def update_setting_in_test_config_file(setting: str, value: Any) -> None:
    """Set the value of a setting in the test config file"""
    yaml.set(
        filepath=get_test_config_file(),
        setting=setting,
        value=value,
        logger=None,
        section="web3cli",
    )


def get_random_string(
    n: int = 6, set: str = string.ascii_lowercase + string.digits
) -> str:
    """Return a random string of length 'n', picking characters from
    the given set"""
    return "".join(secrets.choice(set) for _ in range(n))
