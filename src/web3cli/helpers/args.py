from cement import App

from web3cli.exceptions import Web3CliError
from web3core.exceptions import RpcIsInvalid
from web3core.helpers.rpc import is_rpc_uri_valid
from web3core.models.chain import Chain
from web3core.models.signer import Signer


def parse_global_args(app: App) -> None:
    """Extend the app object with global arguments. Must be
    run post argument parsing"""

    app.extend("signer", parse_signer(app))
    app.extend("priority_fee", parse_priority_fee(app))
    app.extend("rpc", parse_rpc(app))
    app.extend("chain_name", parse_chain(app))
    app.extend("chain", Chain.get_by_name(app.chain_name))


def get_command(app: App) -> str:
    """Return the command passed to the CLI, using dot notation.
    For example, if the CLI is invoked as `w3 db chain list` the
    function will return the string `chain.list`.

    Return None if the CLI was invoked without a command"""
    try:
        return app.pargs.__dispatch__
    except:
        return None


def parse_chain(app: App) -> str:
    """Try to infer which chain the user wants to use.

    The following is the order in which the chain is
    discovered and loaded:

    - Argument --chain or -c passed to the CLI
    - Default chain from the config file
    - If there's only one chain in the DB, use it

    Otherwise, raise a Web3CliError."""
    if app.pargs.chain:
        chain = app.pargs.chain
    elif Chain.select().count() == 1:
        chain = Chain.select().get().name
    elif app.config.get("web3cli", "default_chain"):
        chain = app.config.get("web3cli", "default_chain")
    else:
        raise Web3CliError(
            "Could not infer the chain you want to use. Try specifying it with the --chain argument."
        )
    return chain


def parse_rpc(app: App) -> str:
    """If the argument --rpc was passed to the CLI, return it; otherwise,
    return None, in which case the app will automatically determine the
    best RPC to use based on the selected chain"""
    if not app.pargs.rpc:
        return None
    if not is_rpc_uri_valid(app.pargs.rpc):
        raise RpcIsInvalid(f"Given RPC is not valid: {app.pargs.rpc}")
    return app.pargs.rpc


def parse_signer(app: App) -> str:
    """Try to infer which signer the user wants to use.

    The following is the order in which the signer is
    discovered and loaded:

    - Argument --signer or -s passed to the CLI
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
        signer = Signer.select().get().name
    else:
        signer = None
    return signer


def parse_priority_fee(app: App) -> int:
    """If the --priority-fee argument was passed to the CLI, return it; otherwise,
    return its default value from the config file"""
    if app.pargs.priority_fee:
        priority_fee = app.pargs.priority_fee
    else:
        priority_fee = app.config.get("web3cli", "default_priority_fee")
    if not priority_fee:
        raise Web3CliError("Priority fee not defined, should not be here")
    return priority_fee


def override_arg(app: App, arg: str, value: str) -> App:
    """Set the value passed to the given argument, overriding whatever
    value was read from the CLI or inferred from the environment.

    Needs to be called before argument parsing."""

    def post_argument_parsing_callback(a: App) -> None:
        setattr(a.pargs, arg, value)

    app.hook.register("post_argument_parsing", post_argument_parsing_callback)
    return app
