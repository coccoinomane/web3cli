import os
from typing import Any, List
from cement import TestApp
from web3cli import hooks
from web3cli.main import Web3Cli, CONFIG
from web3cli.helpers import database
from tests import helper

# Each time you run the test app, a brand new database
# will be created
CONFIG["web3cli"]["db_file"] = os.path.join(
    os.path.expanduser("~"), ".web3cli", "database", "web3cli_test.sqlite"
)


class Web3CliTest(TestApp, Web3Cli):
    """A sub-class of Web3Cli that is better suited for testing."""

    def __init__(self, label: str = None, delete_db: bool = True, **kw: Any) -> None:
        super().__init__(label, **kw)
        self.delete_db = delete_db == True

    class Meta:
        label = "web3cli"

        config_defaults = CONFIG

        config_files = [
            helper.get_test_config_file(),
        ]

        hooks = [
            ("pre_setup", helper.delete_test_config_file),
            ("post_setup", database.maybe_delete_db_file),
            ("post_setup", hooks.post_setup),
            ("post_argument_parsing", hooks.post_argument_parsing),
        ]

    def set_args(self: Web3Cli, argv: List[str]) -> Web3Cli:
        """Allow to set CLI arguments as app.set_args()"""
        for arg in argv:
            if type(arg) is not str:
                raise Exception("All CLI arguments in tests must be strings")
        self._meta.argv = argv
        return self
