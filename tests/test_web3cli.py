from pytest import raises
from web3cli.main import Web3CliTest


def test_web3cli() -> None:
    # test web3cli without any subcommands or arguments
    with Web3CliTest() as app:
        app.run()
        assert app.exit_code == 0


def test_web3cli_debug() -> None:
    # test that debug mode is functional
    argv = ["--debug"]
    with Web3CliTest(argv=argv) as app:
        app.run()
        assert app.debug is True


def test_network_list() -> None:
    # test command1 without arguments
    argv = ["command1"]
    with Web3CliTest(argv=argv) as app:
        app.run()
        data, output = app.last_rendered
        assert data["foo"] == "bar"
        assert output.find("Foo => bar")

    # test command1 with arguments
    argv = ["command1", "--foo", "not-bar"]
    with Web3CliTest(argv=argv) as app:
        app.run()
        data, output = app.last_rendered
        assert data["foo"] == "not-bar"
        assert output.find("Foo => not-bar")
