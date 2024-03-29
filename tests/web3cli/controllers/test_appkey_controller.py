import ast
import os

import ruamel.yaml

from tests import helper
from tests.web3cli.main import Web3CliTest


def test_appkey_create() -> None:
    with Web3CliTest() as app:
        # Delete config file and unset app_key
        helper.delete_test_config_file(app)
        app.set_option("app_key", None)
        # Run the command `w3 app-key create`
        app.set_args(
            [
                "app-key",
                "create",
            ]
        ).run()
        # Now the config file should exist...
        config_file = helper.get_test_config_file()
        assert os.path.isfile(config_file)
        # ... and it should contain the app key
        yaml = ruamel.yaml.YAML()
        with open(config_file, "r") as file:
            config = yaml.load(file)
        app_key = config["web3cli"]["app_key"]
        assert type(app_key) is str
        assert type(ast.literal_eval(app_key)) is bytes


def test_appkey_update() -> None:
    with Web3CliTest() as app:
        # Take note of the app_key before it is updated
        old_key = app.get_option("app_key")
        # Run the command `w3 app-key create --force`
        app.set_args(
            [
                "app-key",
                "create",
                "--force",
            ]
        ).run()
        # The config file should exist...
        config_file = helper.get_test_config_file()
        assert os.path.isfile(config_file)
        # ... and it should contain the app key
        yaml = ruamel.yaml.YAML()
        with open(config_file, "r") as file:
            config = yaml.load(file)
        app_key = config["web3cli"]["app_key"]
        assert type(app_key) is str
        assert type(ast.literal_eval(app_key)) is bytes
        # .. and the app key should be different to the old app_key
        assert app_key != old_key
