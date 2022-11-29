from tests.main import Web3CliTest


def test_naked() -> None:
    # test web3cli without any subcommands or arguments
    with Web3CliTest() as app:
        app.run()
        assert app.exit_code == 0


def test_debug() -> None:
    # test that debug mode is functional
    argv = ["--debug"]
    with Web3CliTest(argv=argv) as app:
        app.run()
        assert app.debug is True
