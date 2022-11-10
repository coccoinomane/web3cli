from cement import App
from web3cli.core.helpers.networks import is_network_supported
from web3cli.core.exceptions import Web3CliError, SignerNotFound
from web3cli.core.models.signer import Signer
from web3cli.core.helpers.networks import get_coin


def parse_global_args(app: App) -> None:
    """Extend the app object with global arguments. Must be
    run post argument parsing"""

    # Save the network provided by the user
    app.extend("network", parse_network(app))  # ethereum binance etc
    app.extend("coin", get_coin(app.network))  # ETH BNB etc

    # Save the signer provided by the user
    app.extend("signer", parse_signer(app))


def get_command(app: App) -> str:
    """Return the command passed to the CLI, using dot notation.
    For example, if the CLI is invoked as `web3 network list` the
    function will return the string `network.list`.

    Return None if the CLI was invoked without a command"""
    try:
        return app.pargs.__dispatch__
    except:
        return None


def parse_network(app: App) -> str:
    """If the network argument was passed to the CLI, return it; otherwise,
    return its default value from the config file"""
    if app.pargs.network:
        network = app.pargs.network
    else:
        network = app.config.get("web3cli", "default_network")
    if not network:
        network = "ethereum"
    return network


def validate_network(network: str) -> None:
    """Throw error if the given network is not supported"""
    if not is_network_supported(network):
        raise Web3CliError(f"Network '{network}' not supported")


def parse_signer(app: App) -> str:
    """If the signer argument was passed to the CLI, return it; otherwise,
    return its default value from the config file"""
    if app.pargs.signer:
        signer = app.pargs.signer
    else:
        signer = app.config.get("web3cli", "default_signer")
    if not signer:
        signer = None
    return signer
