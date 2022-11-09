from ..main import Web3CliTest
import ast
from tests import helper
import pytest
import ruamel.yaml
import os


@pytest.mark.xfail
def test_key_create() -> None:
    """This fails on my Macbook Pro Intel with this YAML error:
    > UnicodeDecodeError: 'utf-8' codec can't decode byte 0xfd in position 111: invalid start byte
    The command however works fine from the CLI"""
    argv = [
        "key",
        "create",
    ]
    with Web3CliTest(argv=argv) as app:
        # Make sure config file does not exist
        config_file = helper.get_test_config_file()
        assert not os.path.isfile(config_file)
        # Run the command `web3 key create`
        app.run()
        # Now the config file should exist...
        assert os.path.isfile(config_file)
        # ... and it should contain the app key
        yaml = ruamel.yaml.YAML()
        with open(config_file, "r") as file:
            config = yaml.load(file)
        app_key = config["web3cli"]["app_key"]
        assert type(app_key) is str
        assert type(ast.literal_eval(app_key)) is bytes
