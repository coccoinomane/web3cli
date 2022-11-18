from cement import App
from web3cli.core.helpers.networks import is_network_supported, get_coin
from web3cli.core.exceptions import Web3CliError
from web3cli.core.models.signer import Signer


def parse_global_args(app: App) -> None:
    """Extend the app object with global arguments. Must be
    run post argument parsing"""

    app.extend("chain", parse_chain(app))  # ethereum binance etc
    app.extend("coin", get_coin(app.chain))  # ETH BNB etc
    app.extend("signer", parse_signer(app))
    app.extend("priority_fee", parse_priority_fee(app))


def get_command(app: App) -> str:
    """Return the command passed to the CLI, using dot notation.
    For example, if the CLI is invoked as `web3 chain list` the
    function will return the string `chain.list`.

    Return None if the CLI was invoked without a command"""
    try:
        return app.pargs.__dispatch__
    except:
        return None


def parse_chain(app: App) -> str:
    """If the chain argument was passed to the CLI, return it; otherwise,
    return its default value from the config file"""
    if app.pargs.chain:
        chain = app.pargs.chain
    else:
        chain = app.config.get("web3cli", "default_chain")
    if not chain:
        raise Web3CliError("Chain not defined, should not be here")
    return chain


def validate_chain(chain: str) -> None:
    """Throw error if the given chain is not supported"""
    if not is_network_supported(chain):
        raise Web3CliError(f"Chain '{chain}' not supported")


def parse_signer(app: App) -> str:
    """Try to infer which signer the user wants to use.

    The following is the order in which the signer is
    discovered and loaded:

    - Signer argument passed to the CLI
    - Default signer from the config file
    - If there's only one signer in the DB, use it

    Otherwise, return None, and leave to the app the
    responsibility to raise an error. We do not raise
    it here because we don't know yet whether the command
    invoked by the user really needs a signer.
    """
    if app.pargs.signer:
        signer = app.pargs.signer
    elif app.config.get("web3cli", "default_signer"):
        signer = app.config.get("web3cli", "default_signer")
    elif Signer.select().count() == 1:
        signer = Signer.select().get().label
    else:
        signer = None
    return signer


def parse_priority_fee(app: App) -> int:
    """If the priority_fee argument was passed to the CLI, return it; otherwise,
    return its default value from the config file"""
    if app.pargs.priority_fee:
        priority_fee = app.pargs.priority_fee
    else:
        priority_fee = app.config.get("web3cli", "default_priority_fee")
    if not priority_fee:
        raise Web3CliError("Priority fee not defined, should not be here")
    return priority_fee
