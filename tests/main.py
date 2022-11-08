from cement import TestApp
from web3cli.main import Web3Cli
from web3cli.helpers import database
from .helper import get_config_filepath, delete_configuration_file


class Web3CliTest(TestApp, Web3Cli):
    """A sub-class of Web3Cli that is better suited for testing."""

    class Meta:
        label = "web3cli"

        config_files = [
            get_config_filepath(),
        ]

        hooks = [
            # Delete the configuration file every single run of the CLI
            ("post_setup", delete_configuration_file),
            ("post_setup", database.attach_testing_db),
        ]

        # if True, delete test db before any run
        reset_db = True
