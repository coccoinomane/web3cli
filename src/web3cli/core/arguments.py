from cement import App
from web3cli.src.helpers.networks import is_network_supported
from web3cli.core.exceptions import Web3CliError


def add_global_arguments(app: App) -> None:
    """Register those arguments that can be specified for
    any command"""
    app.args.add_argument(
        "-n",
        "--network",
        help="network (blockchain) to use",
        action="store",
        dest="network",
    )


def handle_global_arguments(app: App) -> None:
    """Do stuff with the values passed for the global arguments.
    Callback for the post_argument_parsing hook"""

    # Store the 'network' argument as an app-level variable
    network = (
        app.pargs.network
        if app.pargs.network
        else app.config.get("web3cli", "default_network")
    )
    if not is_network_supported(network):
        raise Web3CliError(f"Network '{network}' not supported")
    app.extend("network", network)
