"""Helper functions to better run tests"""

import os
import secrets
import string

from web3cli.framework.app import App


def get_test_config_file() -> str:
    """Path to the config file that the app will use while running tests"""
    return os.path.join(
        os.path.expanduser("~"), ".web3cli", "config", "web3cli_test.yml"
    )


def delete_test_config_file(app: App) -> None:
    """Delete the configuration file for the test app"""
    file = get_test_config_file()
    if os.path.isfile(file):
        os.remove(file)


def get_random_string(
    n: int = 6, set: str = string.ascii_lowercase + string.digits
) -> str:
    """Return a random string of length 'n', picking characters from
    the given set"""
    return "".join(secrets.choice(set) for _ in range(n))
