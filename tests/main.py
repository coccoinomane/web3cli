from cement import TestApp
from web3cli.main import Web3Cli, CONFIG
from web3cli.helpers import database
from tests import helper
import os

# Each time you run the test app, a brand new database
# will be created
CONFIG["web3cli"]["db_file"] = helper.get_test_config_file()


class Web3CliTest(TestApp, Web3Cli):
    """A sub-class of Web3Cli that is better suited for testing."""

    class Meta:
        label = "web3cli"

        config_defaults = CONFIG

        config_files = [
            helper.get_test_config_file(),
        ]

        hooks = [
            ("pre_setup", helper.delete_test_config_file),
            ("post_setup", database.delete_db_file),
            ("post_setup", database.attach_db),
        ]
