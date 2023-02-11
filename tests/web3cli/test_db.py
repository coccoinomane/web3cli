from cement import fs

from tests.web3cli.main import CONFIG, Web3CliTest
from web3core.models.chain import Chain
from web3core.models.contract import Contract


def test_db_creation() -> None:
    """DB should be created after setup, no need to run the app."""
    with Web3CliTest() as app:
        assert app.db.database == CONFIG["web3cli"]["db_file"]


def test_db_creation_with_custom_db_path(tmp: fs.Tmp) -> None:
    CONFIG["web3cli"]["db_file"] = f"{tmp.dir}/web3cli.sqlite"
    with Web3CliTest() as app:
        assert app.db.database == f"{tmp.dir}/web3cli.sqlite"


def test_db_is_populated() -> None:
    """When populate_db is True, DB should contain some chains
    and contracts after setup"""
    CONFIG["web3cli"]["populate_db"] = True
    with Web3CliTest() as app:
        assert len(Chain.get_all()) > 0
        assert len(Contract.get_all()) > 0


def test_db_is_not_populated() -> None:
    """When populate_db is False, DB should not contain any chains
    or contracts after setup"""
    CONFIG["web3cli"]["populate_db"] = False
    with Web3CliTest() as app:
        assert len(Chain.get_all()) == 0
        assert len(Contract.get_all()) == 0
