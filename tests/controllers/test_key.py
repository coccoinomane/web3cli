from tests.main import Web3CliTest
import ast
from tests import helper
import ruamel.yaml
import os


def test_key_create() -> None:
    with Web3CliTest() as app:
        # Delete config file and unset app_key
        helper.delete_test_config_file(app)
        app.config.set("web3cli", "app_key", None)
        # Run the command `w3 key create`
        app.set_args(
            [
                "key",
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


def test_key_update() -> None:
    with Web3CliTest() as app:
        # Take note of the app_key before it is updated
        old_key = app.config.get("web3cli", "app_key")
        # Run the command `w3 key create --force`
        app.set_args(
            [
                "key",
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
