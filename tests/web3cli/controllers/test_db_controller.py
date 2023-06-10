import os

from cement import fs

from tests.web3cli.main import CONFIG, Web3CliTest


def test_db_where(tmp: fs.Tmp) -> None:
    # Test with default path
    with Web3CliTest() as app:
        app.set_args(["db", "where"]).run()
        data, output = app.last_rendered
        assert data == CONFIG["web3cli"]["db_file"]

    # Test with custom path
    CONFIG["web3cli"]["db_file"] = f"{tmp.dir}/web3cli.sqlite"
    with Web3CliTest() as app:
        app.set_args(["db", "where"]).run()
        data, output = app.last_rendered
        assert data == f"{tmp.dir}/web3cli.sqlite"


def test_db_delete(tmp: fs.Tmp) -> None:
    # Test with default path
    with Web3CliTest() as app:
        app.set_args(["db", "delete", "--force"]).run()
        assert not os.path.isfile(app.db.database)

    # Test with custom path
    with Web3CliTest() as app:
        CONFIG["web3cli"]["db_file"] = f"{tmp.dir}/web3cli.sqlite"
        app.set_args(["db", "delete", "--force"]).run()
        assert not os.path.isfile(app.db.database)
