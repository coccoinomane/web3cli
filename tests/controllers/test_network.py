from web3cli.main import Web3CliTest


def test_network_list() -> None:
    argv = ["network", "list"]
    with Web3CliTest(argv=argv) as app:
        app.run()
        data, output = app.last_rendered
        assert "ethereum" in output
